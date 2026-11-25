"""Abre o Chrome/Chromium do Playwright. Usa o Chrome do sistema se existir.
Se faltar: pip install playwright && playwright install chromium"""
import os
from playwright.sync_api import sync_playwright

def launch(p):
    for exe in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if os.path.exists(exe):
            return p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
    return p.chromium.launch(args=["--no-sandbox"])
