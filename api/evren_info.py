"""EVREN LLM API handler — connection status, quota, terms.

Route: /api/plugins/evren_llm/evren_info
"""
from __future__ import annotations

from helpers.api import ApiHandler, Request, Response

from usr.plugins.evren_llm.helpers import evren_client


class EvrenInfo(ApiHandler):

    async def process(self, input: dict, request: Request) -> dict | Response:
        api_key = str(input.get("api_key", "") or "").strip()
        action = str(input.get("action", "") or "status").strip()
        if not api_key:
            return {"ok": False, "error": "api_key_required"}
        try:
            if action == "test":
                return evren_client.test_connection(api_key)
            if action == "terms":
                return {"ok": True, "terms": evren_client.get_terms_status(api_key)}
            if action == "terms_text":
                return {"ok": True, "terms": evren_client.get_terms_text(api_key)}
            if action == "accept_terms":
                version = int(input.get("version") or 1)
                return {"ok": True, "result": evren_client.accept_terms(api_key, version)}
            if action == "quota":
                return {"ok": True, "quota": evren_client.get_quota(api_key)}

            # default: full status snapshot
            conn = evren_client.test_connection(api_key)
            out = {"ok": True, "connection": conn}
            if conn.get("ok"):
                try:
                    out["quota"] = evren_client.get_quota(api_key)
                except Exception as exc:
                    out["quota_error"] = str(exc)
            return out
        except Exception as exc:
            return Response(status=500, response=str(exc))
