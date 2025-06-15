import requests
import os

os.makedirs("assets", exist_ok=True)
url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
r = requests.get(url)

with open("assets/world-countries.json", "w", encoding="utf-8") as f:
    f.write(r.text)

print("✅ GeoJSON file saved to assets/world-countries.json")
