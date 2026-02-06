#!/usr/bin/env python3
"""Capture full-page screenshots of the Tractor app using Playwright.

Usage:
  source .venv/bin/activate
  python scripts/screenshot.py

Environment variables:
  TRACTOR_HOST - host to connect to (default: 127.0.0.1)
  TRACTOR_PORT - port to connect to (default: 5000)
"""
import os
from playwright.sync_api import sync_playwright

HOST = os.environ.get('TRACTOR_HOST', '127.0.0.1')
PORT = os.environ.get('TRACTOR_PORT', '5000')
BASE = f'http://{HOST}:{PORT}'


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 900})

        # Home
        page.goto(f'{BASE}/', timeout=60000)
        page.screenshot(path='full_screenshot_home.png', full_page=True)

        # Fill sample form and submit
        page.fill('input[name="acres"]', '150')
        try:
            page.check('input[name="terrain"][value="flat"]')
        except Exception:
            pass
        try:
            page.check('input[name="tasks"][value="loader"]')
        except Exception:
            pass
        try:
            page.select_option('select[name="budget"]', 'medium')
        except Exception:
            pass

        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle', timeout=60000)
        page.screenshot(path='full_screenshot_recommend.png', full_page=True)

        browser.close()
    print('WROTE full_screenshot_home.png and full_screenshot_recommend.png')


if __name__ == '__main__':
    main()
