from collections import Counter
from math import inf


alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'

def addition(word: str, words) -> list[str]:
  candidates = []
  for i in range(len(word) + 1):
    for c in alphabet:
      candidate = word[:i] + c + word[i:]
      if candidate in words:
         candidates.append(candidate)
  return candidates

def deletion(word: str, words) -> list[str]:
   candidates = []
   for i in range(len(word)):
     candidate = word[:i] + word[i+1:]
     if candidate in words:
      candidates.append(candidate)
   return candidates 

def transposition(word: str, words) -> list[str]:
  candidates = []
  for i in range(len(word)):
      if i < len(word) - 1:
        candidate = word[:i] + word[i+1] + word[i] + word[i+2:]
        if candidate in words:
          candidates.append(candidate)
  return candidates

def substitution(word: str, words) -> list[str]:
  candidates = []
  for i in range(len(word)):
     for c in alphabet:
        if c != word[i]:
           candidate = word[:i] + c + word[i+1:]
           if candidate in words:
            candidates.append(candidate)
  return candidates

def find_candidates(word: str, words) -> list[str]:
   cand_set = set()
   cand_set.update(addition(word, words))
   cand_set.update(deletion(word, words))
   cand_set.update(substitution(word, words))
   cand_set.update(transposition(word, words))
   return list(cand_set)

def find_best_candidate(word, candidates, freqs):
   best_word=word
   best = 0
   for candidate in candidates:
       freq = freqs.get(candidate, -inf)
       if freq > best:
          best_word = candidate
          best = freq
   return best_word

def calc_freqs(words):
   counter = Counter(words)
   N = len(counter.items())
   freqs = {word: count / N for word, count in counter.items()} 
   return freqs

def main():
    with open("./data/sv_words.txt", "r") as f:
       text = f.read().splitlines()
       freqs = calc_freqs(text)
    
    with open("./texts/in.txt", "r") as f:
       res = []
       text = f.read().split()
       for word in text:
          res.append(find_best_candidate(word, find_candidates(word, list(freqs.keys())), freqs))
    
    with open("./texts/out.txt", "w") as f:
       f.write(" ".join(res))
          
    


if __name__ == "__main__":
    main()
      