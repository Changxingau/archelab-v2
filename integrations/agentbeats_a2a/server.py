from __future__ import annotations
import argparse
import json
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional

from archerisk_core.episode_schema import Episode
from archerisk_core.runner import simulate_episode

# In-memory task store (sufficient for local AgentBeats-style harness)
TASKS: Dict[str, Dict[str, Any]] = {}
LOCK = threading.Lock()

def agent_card(base_url: str) -> Dict[str, Any]:
    return {
        "name": "ArcheRisk-Core Agent",
        "description": "ArcheRisk-Core benchmark agent (purple) with A2A JSON-RPC interface.",
        "url": base_url + "/",
        "version": "0.4.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": [
            {
                "name": "run_episode",
                "description": "Runs one ArcheRisk-Core episode and returns an EpisodeResult artifact.",
                "tags": ["benchmark", "security", "mas", "evaluation"]
            }
        ]
    }

def _make_task(task_id: str, state: str, artifact: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "id": task_id,
        "status": {"state": state, "timestamp": time.time()},
        "artifacts": [artifact] if artifact else [],
    }

class Handler(BaseHTTPRequestHandler):
    server_version = "ArcheRiskA2A/0.4"

    def _send(self, code: int, payload: Any, content_type: str = "application/json") -> None:
        body = payload if isinstance(payload, (bytes, bytearray)) else json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/.well-known/agent.json":
            host = self.headers.get("Host", "localhost")
            base = f"http://{host}"
            return self._send(200, agent_card(base))
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/":
            return self._send(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8")
        try:
            req = json.loads(raw)
        except Exception:
            return self._send(400, {"error": "invalid json"})

        rpc_id = req.get("id", None)
        method = req.get("method", "")
        params = req.get("params", {}) or {}

        try:
            if method in ("message/send", "tasks/send"):
                # Accept either a "task.id" or create one
                task_id = None
                if isinstance(params, dict):
                    t = params.get("task", {}) or {}
                    task_id = t.get("id")
                if not task_id:
                    task_id = str(uuid.uuid4())

                # Extract Episode from message parts (DataPart)
                msg = params.get("message", {}) or {}
                parts = msg.get("parts", []) or []
                ep_obj = None
                for p in parts:
                    if p.get("kind") == "data":
                        data = p.get("data", {}) or {}
                        if "episode" in data:
                            ep_obj = data["episode"]
                            break
                if ep_obj is None:
                    raise ValueError("missing data.part.data.episode")

                ep = Episode(**ep_obj)

                # Mark running
                with LOCK:
                    TASKS[task_id] = _make_task(task_id, "running")

                # Run synchronously (AgentBeats style is usually sync here)
                res = simulate_episode(ep, out_trace_dir="runs/traces_a2a")
                artifact = {
                    "id": "episode_result",
                    "name": "EpisodeResult",
                    "parts": [{"kind": "data", "data": {"episode_result": res.to_dict()}}],
                }
                task = _make_task(task_id, "completed", artifact)

                with LOCK:
                    TASKS[task_id] = task

                resp = {"jsonrpc": "2.0", "id": rpc_id, "result": task}
                return self._send(200, resp)

            if method in ("tasks/get",):
                task_id = params.get("id") or params.get("taskId")
                if not task_id:
                    raise ValueError("missing task id")
                with LOCK:
                    task = TASKS.get(task_id)
                if not task:
                    raise ValueError("unknown task id")
                resp = {"jsonrpc": "2.0", "id": rpc_id, "result": task}
                return self._send(200, resp)

            # unknown method
            resp = {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32601, "message": "Method not found"}}
            return self._send(200, resp)

        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32602, "message": str(e)}}
            return self._send(200, resp)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    srv = HTTPServer((args.host, args.port), Handler)
    print(f"[A2A] ArcheRisk-Core server on http://{args.host}:{args.port}/")
    print(f"[A2A] agent card: http://{args.host}:{args.port}/.well-known/agent.json")
    srv.serve_forever()

if __name__ == "__main__":
    main()
