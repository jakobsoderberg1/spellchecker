from collections import Counter
from math import inf
import regex as re


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
    with open("./data/bigram_freqs.txt", "r") as f:
       text = f.read().splitlines()
       bigam_freqs = {(line.split()[0], line.split()[1]): float(line.split()[2].strip()) for line in text}
    corrected = []
    text = open("./texts/in.txt", "r").read()
    pattern = r'(?<=[\.\!\?][»”")\]]?)\s+(?=[\p{L}])'
    text = re.sub(pattern, r' </s> <s> ', text, flags=re.UNICODE).strip()
    text = text.replace(".", "")
    text = ['<s>'] + text.lower().split() + ['</s>']

    for word in text:
      if word not in unigram_freqs.keys() and word != '<s>' and word != '</s>':
        corrected.append(find_best_candidate(word, find_candidates(word, list(unigram_freqs.keys())), unigram_freqs))
      else:
          corrected.append(word)
    
    for i in range(len(corrected) - 1):
       if corrected[i] == '<s>':
          corrected[i+1] = corrected[i+1].capitalize()
    corrected = " ".join(corrected[1:-1])
    corrected = re.sub(r' </s> <s> ', ". ", corrected)    
    with open("./texts/out.txt", "w") as f:
       f.write(corrected)
          
    


if __name__ == "__main__":
    main()
      