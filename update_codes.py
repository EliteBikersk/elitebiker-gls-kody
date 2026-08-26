#!/usr/bin/env python3
"""Stiahne dostupnostny feed Sloger a ulozi vsetky kody produktov do codes.json."""

import json
import re
import sys
import urllib.request

FEED_URL = "https://www.sloger.sk/feed/xml/60ad8-2964-elitebiker-s-r-o-availabilities"
OUTPUT = "codes.json"

def main():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0 (codes-sync)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        xml = resp.read().decode("utf-8", errors="replace")

    codes = re.findall(r"<code>\s*(.*?)\s*</code>", xml)
    codes = sorted({c.strip().upper() for c in codes if c.strip()})

    if len(codes) < 50:
        # poistka: ak feed vrati podozrivo malo kodov (vypadok, chyba),
        # radsej neprepisujeme existujuci zoznam
        print(f"CHYBA: feed vratil iba {len(codes)} kodov, subor neprepisujem.")
        sys.exit(1)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, separators=(",", ":"))

    print(f"OK: ulozenych {len(codes)} kodov do {OUTPUT}")

if __name__ == "__main__":
    main()
