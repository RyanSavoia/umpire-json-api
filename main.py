from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.thebettinginsider.com"],  # Your website domain
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)

@app.get("/")
async def get_umpire_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.new_page()
        await page.goto("https://swishanalytics.com/mlb/mlb-umpire-factors", timeout=60000)
        await page.wait_for_timeout(5000)  # Let page fully load
        
        # Get data from the SECOND table (index 1)
        data = await page.evaluate('''
            () => {
                const table = document.querySelectorAll('table')[1];
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                return rows.map(row => {
                    const cells = Array.from(row.querySelectorAll('td'));
                    return {
                        umpire: cells[0]?.textContent.trim(),
                        matchup: cells[1]?.textContent.trim(),
                        games: cells[2]?.textContent.trim(),
                        k_pct: cells[3]?.textContent.trim(),
                        bb_pct: cells[4]?.textContent.trim(),
                        rpg: cells[5]?.textContent.trim(),
                        ba: cells[6]?.textContent.trim(),
                        obp: cells[7]?.textContent.trim(),
                        slg: cells[8]?.textContent.trim(),
                        k_boost: cells[9]?.textContent.trim(),
                        bb_boost: cells[10]?.textContent.trim(),
                        r_boost: cells[11]?.textContent.trim(),
                        ba_boost: cells[12]?.textContent.trim(),
                        obp_boost: cells[13]?.textContent.trim(),
                        slg_boost: cells[14]?.textContent.trim()
                    };
                });
            }
        ''')
        
        await browser.close()
        return data

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
