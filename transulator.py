import time
import tracemalloc
import csv

start_time = time.time()
tracemalloc.start()

frenchDictFile = open("french_dictionary.csv")
frenchDictReader = csv.reader(frenchDictFile)
findWordFile = open("find_words.txt")
transulateFile = open("t8.shakespeare.txt", "r+")
frenchDict = dict()
wordFreq = dict()
for row in frenchDictReader:
  frenchDict[row[0]] = row[1]

text = transulateFile.read()
transulateFile.seek(0)
word = ""
for char in text:
  if char.isalpha():
    word += char
  elif word:
    lowerWord = word.lower()
    frenchWord = frenchDict.get(lowerWord, "")
    if not frenchWord:
      transulateFile.write(word + char)
    elif word.istitle():
      transulateFile.write(frenchWord.title() + char)
      wordFreq[lowerWord] = wordFreq.get(lowerWord, 0) + 1
    elif word.isupper:
      transulateFile.write(frenchWord.upper() + char)
      wordFreq[lowerWord] = wordFreq.get(lowerWord, 0) + 1
    else:
      transulateFile.write(frenchWord + char)
      wordFreq[lowerWord] = wordFreq.get(lowerWord, 0) + 1
    word = ""
  else:
    transulateFile.write(char)

with open("word_freq.txt", "w") as wfFile:
  for key, value in wordFreq.items():
    wfFile.write("{} => {}\n".format(key, value))

print("Time taken to transulate the file =", (time.time() - start_time))
current, peak = tracemalloc.get_traced_memory()
print("Memory usage is {}KB; Peak was {}KB".format(current / 1024, peak / 1024))
print("List of words replaced:")
print(wordFreq.keys())
print("See the frequency of the words replaced in word_freq.txt")

transulateFile.close()
findWordFile.close()
frenchDictFile.close()