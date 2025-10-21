# fetch_stats.py
import csv, time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

PLAYER_NAMES = ["Shai Gilgeous-Alexander","Luka Doncic"]
SEASONS = ["2024-25"]

def get_player_id(name):
    allp = players.get_players()
    for p in allp:
        if p["full_name"].lower()==name.lower(): return p["id"]
    for p in allp:
        if name.lower() in p["full_name"].lower(): return p["id"]
    raise ValueError("player not found: "+name)

def fetch():
    rows=[]
    for name in PLAYER_NAMES:
        try:
            pid = get_player_id(name)
        except Exception as e:
            print("skip",name,e); continue
        for season in SEASONS:
            time.sleep(0.6)
            gl = playergamelog.PlayerGameLog(player_id=pid, season=season)
            df = gl.get_data_frames()[0]
            for _,r in df.iterrows():
                rows.append({
                    "player_name": r["PLAYER_NAME"],
                    "game_date": str(r["GAME_DATE"]),
                    "points": r["PTS"],
                    "assists": r["AST"],
                    "rebounds": r["REB"],
                    "minutes": r["MIN"],
                    "matchup": r["MATCHUP"]
                })
    keys = ["player_name","game_date","points","assists","rebounds","minutes","matchup"]
    with open("player_stats_fetched.csv","w",newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote player_stats_fetched.csv", len(rows))

if __name__=="__main__":
    fetch()
