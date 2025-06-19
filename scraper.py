from fastapi import FastAPI
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/")
def get_umpire_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://swishanalytics.com/mlb/mlb-umpire-factors", timeout=60000)
        page.wait_for_selector("table")  # Wait for the table to render
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    rows = table.find_all("tr")[2:]  # skip header rows

    data = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 13:
            continue
        data.append({
            "umpire": cells[0].get_text(strip=True),
            "matchup": cells[1].get_text(strip=True),
            "k_boost": cells[8].get_text(strip=True),
            "bb_boost": cells[9].get_text(strip=True),
            "r_boost": cells[10].get_text(strip=True),
            "ba_boost": cells[11].get_text(strip=True),
            "obp_boost": cells[12].get_text(strip=True),
            "slg_boost": cells[13].get_text(strip=True),
        })

    return data
