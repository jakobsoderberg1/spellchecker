import requests, time, collections, re, random, json, sys
import regex as re
from requests.adapters import HTTPAdapter
from pathlib import Path
from urllib3.util.retry import Retry

TARGET_TOKENS = 100_000   
SLEEP_SEC = 0.35          
OUT_DIR = Path("data"); OUT_DIR.mkdir(exist_ok=True)

WORD_RE = r"\p{L}+"

UA = "SpellcheckerScraper/0.1 (https://github.com/jakobsoderberg1/yourrepo; jakob.soderberg9@gmail.com)"

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
    url = "https://sv.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "random",
        "grnnamespace": 0,
        "prop": "extracts",
        "explaintext": 1,
        "format": "json"
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return ""
    # There’s exactly one random page
    page = next(iter(pages.values()))
    return page.get("extract", "") or ""

def tokenize(text):
    # Keep words made only of letters; casefold preserves å/ä/ö semantics well
    for match in re.finditer(WORD_RE, text):
        yield match.group(0).casefold()


def main():
    token_list = []
    freqs = collections.Counter()
    while len(token_list) < TARGET_TOKENS:
      txt = fetch_random_svwiki_plaintext()
      if not txt:
        time.sleep(SLEEP_SEC); continue
      for w in tokenize(txt):
        token_list.append(w)
        freqs[w] += 1
        if len(token_list) >= TARGET_TOKENS:
          break
        time.sleep(SLEEP_SEC)

    # Shuffle tokens to de-correlate page order
    random.shuffle(token_list)

    # Write outputs
    (OUT_DIR / "sv_tokens.txt").write_text("\n".join(token_list), encoding="utf-8")
    with (OUT_DIR / "sv_freqs.tsv").open("w", encoding="utf-8") as f:
        for w, c in freqs.most_common():
            f.write(f"{w}\t{c}\n")

    # Small summary on stdout
    print(f"Collected tokens: {len(token_list)}")
    print(f"Unique types: {len(freqs)}")
    print("Top 20:", freqs.most_common(20))

if __name__ == "__main__":
    main()
