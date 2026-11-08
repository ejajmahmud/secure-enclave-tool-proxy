"""Unit tests for secure-enclave-tool-proxy."""
import unittest
from secure_enclave_tool_proxy.proxy import SecureEnclaveToolProxy


class TestSecureEnclaveToolProxy(unittest.TestCase):
    def test_sign_payload_success(self):
        p = SecureEnclaveToolProxy()
        p.register_key("k1", b"secret", ["sign_sha256"])
        res = p.sign_payload("k1", "sign_sha256", "data123")
        self.assertTrue(res["success"])
        self.assertIn("signature", res)

    def test_disallowed_operation(self):
        p = SecureEnclaveToolProxy()
        p.register_key("k1", b"secret", ["sign_sha256"])
        res = p.sign_payload("k1", "delete_all", "data123")
        self.assertFalse(res["success"])
