from playwright.sync_api import sync_playwright
import os, pathlib

html = pathlib.Path("C:/Users/adamb/Desktop/crypto-market-monitor/docs/report/rapport.html").resolve()
out  = str(pathlib.Path("C:/Users/adamb/Desktop/crypto-market-monitor/docs/report/crypto-market-monitor-rapport-technique.pdf").resolve())

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("file:///" + str(html).replace("\\", "/"), wait_until="networkidle")
    page.wait_for_timeout(2500)
    page.pdf(
        path=out,
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    browser.close()
    size = os.path.getsize(out) // 1024
    print("PDF saved -> " + out + " (" + str(size) + " KB)")
