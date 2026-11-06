"""EVREN LLM Provider — lifecycle hooks.

No external dependencies required; uses stdlib + httpx (already in A0).
"""


def install() -> bool:
    return True


def pre_update() -> bool:
    return True


def uninstall() -> bool:
    return True
