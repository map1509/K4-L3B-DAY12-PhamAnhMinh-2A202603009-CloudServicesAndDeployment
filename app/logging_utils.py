from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, level: str = "info", **fields) -> str:
    payload = {"event": event, "level": level.lower(), "timestamp": utc_now_iso(), **fields}
    serialized = json.dumps(payload, ensure_ascii=False)
    print(serialized, file=sys.stdout)
    return serialized
