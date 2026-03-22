import urllib.request
import urllib.parse
import json
import time
import sys

# Load existing results
with open("image_urls.json") as f:
    existing = json.load(f)

# Find entries with empty URLs
missing = {k: v for k, v in existing.items() if not v}
print(f"Retrying {len(missing)} missing entries...", file=sys.stderr)

for i, key in enumerate(missing):
    artist, query = key.split("|", 1)
    try:
        encoded = urllib.parse.quote(query)
        # Try commons first this time
        url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srnamespace=6&srlimit=1&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            if data.get("query", {}).get("search"):
                file_title = data["query"]["search"][0]["title"]
                url2 = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
                req2 = urllib.request.Request(url2, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                with urllib.request.urlopen(req2, timeout=10) as resp2:
                    data2 = json.loads(resp2.read())
                    pages = data2.get("query", {}).get("pages", {})
                    for page in pages.values():
                        ii = page.get("imageinfo", [{}])[0]
                        thumb = ii.get("thumburl", ii.get("url", ""))
                        if thumb:
                            existing[key] = thumb
                            print(f"[{i+1}/{len(missing)}] OK: {artist}", file=sys.stderr)
                        else:
                            print(f"[{i+1}/{len(missing)}] STILL MISS: {artist}", file=sys.stderr)
            else:
                # Try wikipedia
                url3 = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srnamespace=6&srlimit=1&format=json"
                req3 = urllib.request.Request(url3, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                with urllib.request.urlopen(req3, timeout=10) as resp3:
                    data3 = json.loads(resp3.read())
                    if data3.get("query", {}).get("search"):
                        file_title3 = data3["query"]["search"][0]["title"]
                        url4 = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title3)}&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
                        req4 = urllib.request.Request(url4, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                        with urllib.request.urlopen(req4, timeout=10) as resp4:
                            data4 = json.loads(resp4.read())
                            pages4 = data4.get("query", {}).get("pages", {})
                            for p4 in pages4.values():
                                ii4 = p4.get("imageinfo", [{}])[0]
                                thumb4 = ii4.get("thumburl", ii4.get("url", ""))
                                if thumb4:
                                    existing[key] = thumb4
                                    print(f"[{i+1}/{len(missing)}] OK (wp): {artist}", file=sys.stderr)
                                else:
                                    print(f"[{i+1}/{len(missing)}] STILL MISS: {artist}", file=sys.stderr)
                    else:
                        print(f"[{i+1}/{len(missing)}] STILL MISS: {artist}", file=sys.stderr)
    except Exception as e:
        print(f"[{i+1}/{len(missing)}] ERROR: {artist} - {e}", file=sys.stderr)
    time.sleep(1.5)

# Save updated
with open("image_urls.json", "w") as f:
    json.dump(existing, f, indent=2)

found = sum(1 for v in existing.values() if v)
print(f"\nTotal found: {found}/{len(existing)}", file=sys.stderr)
