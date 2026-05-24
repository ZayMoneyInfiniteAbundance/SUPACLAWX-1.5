#!/usr/bin/env python3
from pathlib import Path
from publisher import build_store_page, build_admin_page
from config import OUTPUT_DIR


def main():
    print("Building NemoClaw Intelligence Vault...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    html = build_store_page()
    index_path = OUTPUT_DIR / "index.html"
    index_path.write_text(html)
    print(f"Store page: {index_path}")

    admin_html = build_admin_page()
    admin_path = OUTPUT_DIR / "admin.html"
    admin_path.write_text(admin_html)
    print(f"Admin page: {admin_path}")

    print("Run 'python3 server.py' to start the server")


if __name__ == "__main__":
    main()
