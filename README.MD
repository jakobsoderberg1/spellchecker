# Spellchecker

After taking the course EDAN20, Language Technology at LTH, I was really inspired how you could create such powerful tools using such few lines of code. As inspiration for this project, I used [Norvigs spelling corrector](https://www.norvig.com/spell-correct.html).

**Data collection**
To gather data, I extracted 100 000 Swedish words from random wikipedia pages to get a diverse dataset. This dataset was then split in to unigrams and bigrams and the frequencies were calculated.

**Implementation**

_V1_
The first version included only unigram frequencies and the result was not very good. I tried the sentence: "Jga hteer Jakob okh spelart handboll i Lund" and the resulting output was "jag heter jakob och spelar handboll i lund", which is the correct sentence although in lower case. To battle this, I opted for a bigram solution which would handle beginning and ending of sentences.

_V2_
The next version I added capitalization and punctuation for sentences. This was however limited to capitalizing the first letter after a start token '<s>' and replacing the previously added sentence separators with a dot. The next step was to fix capitalization for names. To implement this I had to change my unigram frequencies by extracting all words in their typed form. Since all sentences begin with a capital letter I will take this into consideration but this leads to another problem. If a sentence start with a name, the name will be tokenized as lower case. However, since the dataset is so large, I don't think this will affect the outcome.
