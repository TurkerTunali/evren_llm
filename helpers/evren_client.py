"""EVREN LLM API client — quota, terms, and credit info.

Base: https://evren-llmapi.ssyz.org.tr/v1
Auth:  Authorization: Bearer <key>  (or X-API-Key)
"""
from __future__ import annotations

import httpx

BASE_URL = "https://evren-llmapi.ssyz.org.tr/v1"
TIMEOUT = 20


def _headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def get_quota(api_key: str) -> dict:
    """GET /v1/quota — daily tokens, credits, reset time."""
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.get(f"{BASE_URL}/quota", headers=_headers(api_key))
        r.raise_for_status()
        return r.json()


def get_terms_status(api_key: str) -> dict:
    """GET /v1/terms/status — returns current_version and accepted status."""
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.get(f"{BASE_URL}/terms/status", headers=_headers(api_key))
        r.raise_for_status()
        return r.json()


def get_terms_text(api_key: str) -> dict:
    """GET /v1/terms/text — terms body for display."""
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.get(f"{BASE_URL}/terms/text", headers=_headers(api_key))
        r.raise_for_status()
        return r.json()


def accept_terms(api_key: str, version: int) -> dict:
    """POST /v1/terms/accept — one-time per account."""
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.post(
            f"{BASE_URL}/terms/accept",
            headers=_headers(api_key),
            json={"version": version},
        )
        r.raise_for_status()
        return r.json()


def test_connection(api_key: str) -> dict:
    """Lightweight auth + connectivity check via /v1/models."""
    with httpx.Client(timeout=TIMEOUT) as client:
        r = client.get(f"{BASE_URL}/models", headers=_headers(api_key))
        if r.status_code == 200:
            return {"ok": True, "models": len(r.json().get("data", []))}
        if r.status_code == 403:
            return {"ok": False, "error": "terms_not_accepted"}
        if r.status_code == 401:
            return {"ok": False, "error": "invalid_api_key"}
        return {"ok": False, "error": f"HTTP {r.status_code}"}


def extract_credit_headers(headers: dict) -> dict:
    """Pull EVREN credit/quota headers from any response."""
    keys = [
        "x-evren-daily-limit-tokens",
        "x-evren-daily-remaining-tokens",
        "x-evren-daily-reset",
        "x-evren-credits-held",
        "x-evren-credits-remaining",
    ]
    return {k.replace("x-evren-", ""): headers.get(k) for k in keys if k in headers}
