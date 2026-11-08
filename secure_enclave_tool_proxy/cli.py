"""CLI for secure-enclave-tool-proxy."""
import sys
import argparse
from .proxy import SecureEnclaveToolProxy


def main():
    parser = argparse.ArgumentParser(description="Secure Enclave Tool Proxy CLI")
    parser.add_argument("--demo", action="store_true", help="Run enclave tool proxy demo")
    args = parser.parse_args()

    if args.demo:
        proxy = SecureEnclaveToolProxy()
        proxy.register_key("deploy_key", b"super_secure_vault_secret", ["sign_sha256"])

        res = proxy.sign_payload("deploy_key", "sign_sha256", "release_v0.1.0_manifest")
        print(f"[+] Signed Payload via Enclave (Raw key never exposed):\n    {res}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
