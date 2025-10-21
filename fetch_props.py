# fetch_props.py
import os, json, requests, csv
from datetime import datetime, timezone

API_KEY = os.getenv("THE_ODDS_API_KEY")
BASE = "https://api.the-odds-api.com/v4"

def fetch_props():
    url = f"{BASE}/sports/basketball_nba/odds"
    params = {"apiKey": API_KEY, "regions":"us", "markets":"player_props", "oddsFormat":"decimal"}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    rows = []
    for ev in data:
        game_date = ev.get("commence_time","").split("T")[0]
        for m in ev.get("markets",[]):
            if m.get("key")!="player_props": continue
            for o in m.get("outcomes",[]):
                name = o.get("name","")
                price = o.get("price")
                parts = name.strip().rsplit(" ", 1)
                line = None
                if len(parts)==2:
                    try:
                        line = float(parts[1])
                    except:
                        line = None
                rows.append({
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "game_date": game_date,
                    "prop_text": name,
                    "player_name": None if line is None else " ".join(parts[0].split()[:-1]) or parts[0],
                    "line": line,
                    "price": price,
                    "raw": json.dumps(o)
                })
    keys = ["fetched_at","game_date","player_name","prop_text","line","price","raw"]
    with open("player_props_fetched.csv","w",newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote player_props_fetched.csv:", len(rows))

if __name__ == "__main__":
    fetch()
