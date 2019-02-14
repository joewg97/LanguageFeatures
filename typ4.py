import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize, ngrams
from collections import Counter
import operator
import os, sys, re, io, codecs

from nltk.tag import pos_tag

import csv

#nltk.download("gutenberg")
total_chars = 0
total_words = 0
total_vocab = 0
total_sents = 0

csvData = [["Filename", "Date", "Avg Word Length", "Average Sentence Length", "Lexical Diversity", "Spelling Variation"]]


def languageFeatures(filename, csvData, csvFreq, csvBigram, main_dir, date_dir):
    global total_chars
    global total_words
    global total_vocab
    global total_sents
    
    
    filename = filename[:-4]
    #print(filename)
    os.chdir(date_dir)
    with open('phase1.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader = list(csv_reader)
        i = 0
        while csv_reader[i][0] != filename:
            #print(csv_reader[i][0])
            i = i + 1
            
        date = csv_reader[i][2]
    
    csv_file.close()
    
    filename = filename + ".xml"
    
    details = []
    details.append(filename[:-4])
    details.append(date)
        
    
    os.chdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1525-1549")
    f = open(filename, 'r', encoding='utf-8')
    raw = f.read()

    TAG_RE = re.compile(r'<[^>]+>')
    converted = TAG_RE.sub('', raw)
    

    #text_file = open("Output.txt", "w")
    #text_file.write(converted)
    #text_file.close()

    tokens = word_tokenize(converted)
    text = nltk.Text(tokens)

    words = [w.lower() for w in tokens if w != "." and w != ","]
    sents = nltk.sent_tokenize(converted)
    chars = [c.lower() for c in converted]
    
    #tagged_text = pos_tag(converted.split())
    #propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    #adjectives = [word for word,pos in tagged_text if pos == 'JJ']
    #foreignwords = [word for word,pos in tagged_text if pos == 'FW']
    #prepositions = [word for word,pos in tagged_text if pos == 'IN']
    #nouns = [word for word,pos in tagged_text if pos == 'NN']
    #adverbs = [word for word,pos in tagged_text if pos == 'RB']
    #propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    #verbs = [word for word,pos in tagged_text if pos == 'VB']
    #personalpronouns = [word for word,pos in tagged_text if pos == 'PRP']


    num_chars = len(chars)
    num_words = len(words)
    num_vocab = len(set(words))
    num_sents = len(sents)
    
    #num_propernouns = len(propernouns)
    #num_adjectives = len(adjectives)
    #num_foreignwords = len(foreignwords)
    #num_prepositions = len(prepositions)
    #num_nouns = len(nouns)
    #num_adverbs = len(adverbs)
    #num_verbs = len(verbs)
    #num_personalpronouns = len(personalpronouns)


    awl = round(num_chars/num_words)
    asl = round(num_words/num_sents)
    lexdiv = round(num_words/num_vocab)
    spellvar = 0
    
    for w in set(words):
        if not wordnet.synsets(w):
            spellvar = spellvar + 1
    
    total_chars = total_chars + num_chars
    total_words = total_words + num_words
    total_vocab = total_vocab + num_vocab
    total_sents = total_sents + num_sents
    
    sv = spellvar/num_vocab
        
    print("File: " + filename)
    print("Avg. Word Length: ",awl,"Avg. Sentence Length: ",asl,"Lexical Diversity: ",lexdiv,"Spelling Variation: ",sv)

    print("Word Frequency: ")
    word_freq = []
    vocab = set(csvFreq)
    
    vocab_size = len(vocab)
    fdist1 = nltk.FreqDist(words)
    #print(fdist1['reste'])
    #print(fdist1['resteth'])
    
    fdist = nltk.FreqDist(words + csvFreq)
    for x,y in sorted(fdist.most_common(vocab_size)):
        word_freq.append(y-1)
    
    #final_freq = [x for x in word_freq if x in csvFreq]
    #word_freq.insert(0,date)
    #word_freq.insert(0,filename[:-4])
    
    #word_freq = [filename[:-4], date] + word_freq
    print(" ")
    
    
    print("Proper Noun Frequency: ")
    #vocab = set(propernouns)
    #vocab_size = len(vocab)
    #fdist = nltk.FreqDist(propernouns)
    #for x,y in fdist.most_common(vocab_size):
        #print(x,y)
    
    print("Character Ngram Frequency: ")
    #ngram = nltk.FreqDist(vs for word in words
     #   for vs in re.findall(r'[abcdefghijklmnopqrstuvwxyz]{3}', word))
    #for k,v in ngram.most_common():
     #   print (k,v)
    window = ()
    temp = []
    ngrams = []
    for i in converted:
        #if len(window) == 3:
         #   ngrams.append(window)
          #  print(window)
           # window.pop(0)
        #window.append(i)
        if len(temp) == 3:
            window = (temp[0],temp[1],temp[2])
            temp.pop(0)
            ngrams.append(window)
            
        temp.append(i)
        #if i == "\n":
            #print("yowza")
    count = Counter(ngrams)
    #scount = sorted(count.items(), key=operator.itemgetter(1))
    
    word_ngrams = []
    for z in csvNgram:
        found = 0
        for w in sorted(count, key=count.get, reverse=True):
            #print (w, count[w])
            if z == w:
                word_ngrams.append(count[w])
                found = 1
                break
        if found == 0:
            word_ngrams.append('0')

    #word_ngrams.insert(0,date)
    #word_ngrams.insert(0,filename[:-4])
    print(" ")
    
    print("Word Bigrams: ")
    word_bigrams = []
    wbigrams = nltk.bigrams(words)
    bigrams = nltk.FreqDist(wbigrams)
    for z in csvBigram:
        found = 0
        for x,y in bigrams.most_common(500):
            #print(x,y)
            if z == x:
                word_bigrams.append(y)
                found = 1
                break
        if found == 0:
            word_bigrams.append('0')
    
    #word_bigrams.insert(0,date)
    #word_bigrams.insert(0,filename[:-4])
    
    print(" ")
    
    csvData.append([filename, date, awl, asl, lexdiv, sv])
    
    with open('details.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(details)
        #writer.writerow(word_freq)
    
    csvFile.close()
    
    with open('freq.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(word_freq)
        #writer.writerow(word_freq)
    
    csvFile.close()
    
    with open('bigram.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(word_bigrams)
    
    csvFile.close()
    
    with open('ngram.csv', 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(word_ngrams)
    
    csvFile.close()
    return;
#reload(sys)  
#sys.setdefaultencoding('utf8')	
#for filename in os.listdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1700-1724"):
 #   if filename.endswith(".xml"): 
  #      languageFeatures(filename)
   #     continue
    #else:
     #   continue

def freq_headers(filename, csvNgram):
    os.chdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1525-1549")
    f = open(filename, 'r', encoding='utf-8')
    raw = f.read()

    TAG_RE = re.compile(r'<[^>]+>')
    converted = TAG_RE.sub('', raw)
    

    #text_file = open("Output.txt", "w")
    #text_file.write(converted)
    #text_file.close()

    tokens = word_tokenize(converted)
    text = nltk.Text(tokens)

    words = [w.lower() for w in tokens if w != "." and w != ","]
    
    window = ()
    temp = []
    ngrams = []
    for i in converted:
        #if len(window) == 3:
         #   ngrams.append(window)
          #  print(window)
           # window.pop(0)
        #window.append(i)
        if len(temp) == 3:
            window = (temp[0],temp[1],temp[2])
            temp.pop(0)
            ngrams.append(window)
            
        temp.append(i)
        #if i == "\n":
            #print("yowza")
    count = Counter(ngrams)
    #scount = sorted(count.items(), key=operator.itemgetter(1))
    #i = 0
    for w in sorted(count, key=count.get, reverse=True):
        #print (w, count[w])
        #i = i++
        csvNgram.append(w)
    print(" ")
    
    return words;

num_files = 0
all_words = []
main_dir = os.getcwd()
date_dir = main_dir+"/EEBO texts/EEBO texts"


csvNgram = []

for filename in os.listdir(main_dir+"/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1525-1549"):
    if filename.endswith(".xml"): 
        all_words = all_words + freq_headers(filename, csvNgram)
        num_files = num_files + 1
        continue
    else:
        continue

        
csvFreq = []
vocab = set(all_words)
vocab_size = len(vocab)
fdist = nltk.FreqDist(all_words)
#csvFreq.append("Filename")
#csvFreq.append("Date")
for x,y in sorted(fdist.most_common(1000)):
    csvFreq.append(x)
print(" ")

#csvFreq = sorted(csvFreq)
#csvFreq.insert(0,"Date")
#csvFreq.insert(0,"Filename")

details = ["Filename", "Date"]
with open('details.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(details)

csvFile.close()

with open('freq.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvFreq)

csvFile.close()


csvBigram = []

wbigrams = nltk.bigrams(all_words)
bigrams = nltk.FreqDist(wbigrams)
for x,y in bigrams.most_common(1000):
    csvBigram.append(x)
print(" ")
    
csvBigram = sorted(csvBigram)

with open('bigram.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvBigram)

csvFile.close()


csvNgram = set(csvNgram)    
csvNgram = sorted(csvNgram)
#csvNgram.insert(0,"Date")
#csvNgram.insert(0,"Filename")

with open('ngram.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvNgram)

csvFile.close()

num_files = 0

for filename in os.listdir(main_dir+"/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1525-1549"):
    if filename.endswith(".xml"): 
        languageFeatures(filename, csvData, csvFreq, csvBigram, main_dir, date_dir)
        num_files = num_files + 1
        continue
    else:
        continue
        
total_chars = total_chars/num_files
total_words = total_words/num_files
#total_vocab = set(int(total_vocab)/num_files)
total_sents = total_sents/num_files

#print("Overall Avgs: " + "Word Length: " + str(total_chars/total_words) + " Vocab: " + " Sentence Length: " + str(total_words/total_sents))
print(" ")

with open('output.csv', 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

csvFile.close()