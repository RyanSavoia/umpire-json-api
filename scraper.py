from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def get_umpire_data():
    url = "https://swishanalytics.com/mlb/mlb-umpire-factors"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

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
