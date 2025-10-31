# Spellchecker

After taking the course EDAN20, Language Technology at LTH, I was really inspired how you could create such powerful tools using such few lines of code. As inspiration for this project, I used [Norvigs spelling corrector](https://www.norvig.com/spell-correct.html).

** Data collection **
To gather data, I extracted 100 000 Swedish words from random wikipedia pages to get a diverse dataset. This dataset was then split in to unigrams and bigrams and the frequencies were calculated.

** Implementation **
The first version included only unigram frequencies and the result was not very good. I tried the sentence: "Jga hteer Jakob okh spelart handboll i Lund" and the resulting output was "jag heter jakob och spelar handboll i lund", which is the correct sentence although in lower case.
