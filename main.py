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

def main():
    with open("./data/unigram_freqs.txt", "r") as f:
       text = f.read().splitlines()
       unigram_freqs = {line.split()[0]: float(line.split()[1].strip()) for line in text}
    print(unigram_freqs)
    
    with open("./texts/in.txt", "r") as f:
       res = []
       text = f.read().lower().split()
       for word in text:
          if word not in unigram_freqs.keys():
            res.append(find_best_candidate(word, find_candidates(word, list(unigram_freqs.keys())), unigram_freqs))
          else:
             res.append(word)
    
    with open("./texts/out.txt", "w") as f:
       f.write(" ".join(res))
          
    


if __name__ == "__main__":
    main()
      