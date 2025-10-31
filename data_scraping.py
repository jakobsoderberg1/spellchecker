import requests, time
import regex as re
from requests.adapters import HTTPAdapter
from pathlib import Path
from collections import Counter
from urllib3.util.retry import Retry

TARGET_TOKENS = 1000000
SLEEP_SEC = 0.35          
OUT_DIR = Path("data"); OUT_DIR.mkdir(exist_ok=True)


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
    r.raise_for_status()
    data = r.json()
    pages =  data.get("query", {}).get("pages", [])
    if not pages:
        return ""
    return pages[0].get("extract", "").strip()

def tokenize(text):
    pattern = r'(?<=[\.\!\?][»”")\]]?)\s+(?=[\p{Lu}])'
    text = re.sub(pattern, r' </s> <s> ', text, flags=re.UNICODE).strip()
    text = text.replace(".", "")
    tokens = ['<s>'] + text.lower().split() + ['</s>']
    return tokens
def main():
    unigram_list = []
    bigram_list = []
    while len(unigram_list) < TARGET_TOKENS:
      txt = fetch_random_svwiki_plaintext()
      if not txt:
        time.sleep(SLEEP_SEC); continue
      tokens = tokenize(txt)
      unigram_list.extend(tokens)
      for i in range(len(tokens) - 1):
          bigram_list.append((tokens[i], tokens[i+1]))
      if len(unigram_list) >= TARGET_TOKENS:
          break
      time.sleep(SLEEP_SEC)

    unigram_counter = Counter(unigram_list)
    bigram_counter = Counter(bigram_list)
    unigrams = len(unigram_counter.items())
    unigram_freqs = {word: count / unigrams for word, count in unigram_counter.items()}
    bigram_freqs = {bigram: count / unigram_counter[bigram[0]] for bigram, count in bigram_counter.items()}

    with open (f"./{OUT_DIR}/unigram_freqs.txt", "w") as f:
        for unigram, freq in unigram_freqs.items():
            f.write(f"{unigram} {freq}\n")

    with open (f"./{OUT_DIR}/bigram_freqs.txt", "w") as f:
        for bigram, freq in bigram_freqs.items():
            f.write(f"{bigram[0]}, {bigram[1]}, {freq}\n")

    # Small summary on stdout
    print(f"Collected unigrams: {len(unigram_list)}")

if __name__ == "__main__":
    main()
