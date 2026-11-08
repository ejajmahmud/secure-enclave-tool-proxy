"""Core Secure Enclave Tool Proxy implementation."""
import hmac
import hashlib
from typing import Dict, Any, Optional


class SecureEnclaveToolProxy:
    def __init__(self):
        # Handle -> secret_key (isolated in proxy memory, never returned)
        self._enclave_keys: Dict[str, bytes] = {}
        self._allowed_operations: Dict[str, set] = {}

    def register_key(self, handle: str, secret: bytes, allowed_ops: Optional[list] = None):
        self._enclave_keys[handle] = secret
        self._allowed_operations[handle] = set(allowed_ops or ["sign_sha256"])

    def sign_payload(self, handle: str, operation: str, payload: str) -> Dict[str, Any]:
        if handle not in self._enclave_keys:
            return {"success": False, "error": f"Unknown key handle '{handle}'"}

        allowed = self._allowed_operations.get(handle, set())
        if operation not in allowed:
            return {"success": False, "error": f"Operation '{operation}' not permitted for handle"}

        key = self._enclave_keys[handle]
        sig = hmac.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "success": True,
            "handle": handle,
            "signature": sig,
            "algorithm": "HMAC-SHA256"
        }
