"""Refreshes Google's key attestation revocation list for the web verifier.

The list (https://android.googleapis.com/attestation/status) has no CORS headers, so the page cannot fetch it
itself. This writes revocations.json next to index.html, which the page reads; the verifier site's GitHub Action
(.github/workflows/revocations.yml) runs it every day. With --embed it also refreshes the fallback copy inside
index.html, used when revocations.json can't be read.
Run: python verify/update-revocations.py [--embed]
"""
import datetime
import json
import pathlib
import re
import sys
import urllib.request

URL = "https://android.googleapis.com/attestation/status"
HERE = pathlib.Path(__file__).parent

entries = json.load(urllib.request.urlopen(URL, timeout=30))["entries"]
# Every listed key is untrusted, whatever its status (REVOKED or SUSPENDED). Same form as the page reads
# certificate serials: lowercase hex without leading zeros.
serials = sorted({k.lower().lstrip("0") or "0" for k in entries})
if len(serials) < 1000 or not all(re.fullmatch(r"[0-9a-f]{1,64}", s) for s in serials):
    raise SystemExit("unexpected revocation list format")
today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

out = HERE / "revocations.json"
out.write_text(json.dumps({"date": today, "source": URL, "serials": serials}) + "\n", encoding="utf-8", newline="\n")
print(f"{len(serials)} revoked serials written to {out.name}")

if "--embed" in sys.argv[1:]:
    page = HERE / "index.html"
    html = page.read_text(encoding="utf-8")
    html, n1 = re.subn(r'const REVOKED_DATE = "[^"]*";', f'const REVOKED_DATE = "{today}";', html)
    html, n2 = re.subn(r'const REVOKED = new Set\("[^"]*"\.split\(" "\)\);', f'const REVOKED = new Set("{" ".join(serials)}".split(" "));', html)
    if (n1, n2) != (1, 1):
        raise SystemExit("placeholders not found")
    page.write_text(html, encoding="utf-8", newline="\n")
    print("fallback copy in index.html refreshed")
