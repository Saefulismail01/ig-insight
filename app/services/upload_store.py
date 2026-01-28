"""
Upload Data Store

Stores processed upload results keyed by upload_id.

Note:
- This implementation persists to local filesystem (UPLOAD_FOLDER).
- For true serverless/multi-instance deployments, replace with a shared store
  (Redis/Vercel KV/DB).
"""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any, Dict, Optional


def _store_dir(upload_folder: str) -> str:
    return os.path.join(upload_folder, "processed")


def _path_for(upload_folder: str, upload_id: str) -> str:
    return os.path.join(_store_dir(upload_folder), f"{upload_id}.json")


def create_upload_id() -> str:
    return uuid.uuid4().hex


def save_processed_data(upload_folder: str, upload_id: str, data: Dict[str, Any]) -> None:
    os.makedirs(_store_dir(upload_folder), exist_ok=True)
    payload = {
        "_meta": {
            "upload_id": upload_id,
            "saved_at": time.time(),
        },
        "data": data,
    }
    path = _path_for(upload_folder, upload_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)


def load_processed_data(upload_folder: str, upload_id: str) -> Optional[Dict[str, Any]]:
    path = _path_for(upload_folder, upload_id)
    print(f"🔍 DEBUG: Attempting to load data for upload_id: {upload_id}")
    print(f"🔍 DEBUG: Looking in path: {path}")
    
    if not os.path.exists(path):
        print(f"❌ DEBUG: File not found at: {path}")
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    # Backward/forward safety: accept either wrapped or raw
    if isinstance(payload, dict) and "data" in payload:
        return payload.get("data")
    return payload
