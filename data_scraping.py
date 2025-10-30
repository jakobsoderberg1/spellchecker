import requests, time, collections, random, json, sys
import regex as re
from requests.adapters import HTTPAdapter
from pathlib import Path
from urllib3.util.retry import Retry

TARGET_TOKENS = 100000  
SLEEP_SEC = 0.35          
OUT_DIR = Path("data"); OUT_DIR.mkdir(exist_ok=True)

WORD_RE = r"\p{L}+"

UA = "SpellcheckerScraper/0.1 (https://github.com/jakobsoderberg1/spellchecker; jakob.soderberg9@gmail.com)"

def _session_with_retries():
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.headers.update({"User-Agent": UA})
    return s

def fetch_random_svwiki_plaintext():
    # Random article from svwiki, main namespace, plaintext extract
    ses = _session_with_retries()
    url = "https://sv.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "random",
        "grnnamespace": 0,     # main/article namespace
        "prop": "extracts",
        "explaintext": 1,      # plain text, no HTML
        "exsectionformat": "plain",
        "format": "json",
        "formatversion": "2",
        "redirects": 1,
        "grnlimit": 1,
    }
    r = ses.get(url, params=params, timeout=15)
    if r.status_code == 403:
        raise RuntimeError(
            "Wikipedia API returned 403 Forbidden. Make sure your User-Agent is "
            "descriptive and includes a contact URL/email (see UA constant)."
        )
    r.raise_for_status()
    data = r.json()
    pages =  data.get("query", {}).get("pages", [])
    if not pages:
        return ""
    page = pages[0]
    return page.get("extract", "").strip()




def main():
    token_list = []
    while len(token_list) < TARGET_TOKENS:
      txt = fetch_random_svwiki_plaintext()
      if not txt:
        time.sleep(SLEEP_SEC); continue
      token_list.extend(re.findall(WORD_RE, txt))
      if len(token_list) >= TARGET_TOKENS:
          break
      time.sleep(SLEEP_SEC)

    random.shuffle(token_list)

    (OUT_DIR / "sv_words.txt").write_text("\n".join(token_list), encoding="utf-8")

    # Small summary on stdout
    print(f"Collected tokens: {len(token_list)}")

if __name__ == "__main__":
    main()
