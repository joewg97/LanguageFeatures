import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize, ngrams
from collections import Counter
import operator
import os, sys, re, io, codecs

from nltk.tag import pos_tag

#nltk.download("gutenberg")
total_chars = 0
total_words = 0
total_vocab = 0
total_sents = 0

def languageFeatures(filename):
    global total_chars
    global total_words
    global total_vocab
    global total_sents
    
    os.chdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1700-1724")
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
    
    tagged_text = pos_tag(converted.split())
    propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    adjectives = [word for word,pos in tagged_text if pos == 'JJ']
    foreignwords = [word for word,pos in tagged_text if pos == 'FW']
    prepositions = [word for word,pos in tagged_text if pos == 'IN']
    nouns = [word for word,pos in tagged_text if pos == 'NN']
    adverbs = [word for word,pos in tagged_text if pos == 'RB']
    propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    verbs = [word for word,pos in tagged_text if pos == 'VB']
    personalpronouns = [word for word,pos in tagged_text if pos == 'PRP']


    num_chars = len(chars)
    num_words = len(words)
    num_vocab = len(set(words))
    num_sents = len(sents)
    
    num_propernouns = len(propernouns)
    num_adjectives = len(adjectives)
    num_foreignwords = len(foreignwords)
    num_propositions = len(propositions)
    num_nouns = len(nouns)
    num_adverbs = len(adverbs)
    num_verbs = len(verbs)
    num_personalpronouns = len(personalpronouns)


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
    
    
    print("File: " + filename)
    print("Avg. Word Length: ",awl,"Avg. Sentence Length: ",asl,"Lexical Diversity: ",lexdiv,"Spelling Variation: ",(spellvar/num_vocab))

    print("Word Frequency: ")
    vocab = set(words)
    vocab_size = len(vocab)
    fdist = nltk.FreqDist(words)
    for x,y in fdist.most_common(vocab_size):
        print(x,y)
    print(" ")
    
    print("Proper Noun Frequency: ")
    vocab = set(propernouns)
    vocab_size = len(vocab)
    fdist = nltk.FreqDist(propernouns)
    for x,y in fdist.most_common(vocab_size):
        print(x,y)
    
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
    
    for w in sorted(count, key=count.get, reverse=True):
        print (w, count[w])
    print(" ")
    
    print("Word Bigrams: ")
    wbigrams = nltk.bigrams(words)
    bigrams = nltk.FreqDist(wbigrams)
    for x,y in bigrams.most_common(500):
        print(x,y)
    print(" ")
    return;


#reload(sys)  
#sys.setdefaultencoding('utf8')	
#for filename in os.listdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1700-1724"):
 #   if filename.endswith(".xml"): 
  #      languageFeatures(filename)
   #     continue
    #else:
     #   continue


num_files = 0

for filename in os.listdir(os.getcwd()+"/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1700-1724"):
    if filename.endswith(".xml"): 
        languageFeatures(filename)
        num_files = num_files + 1
        continue
    else:
        continue
        
total_chars = total_chars/num_files
total_words = total_words/num_files
#total_vocab = set(int(total_vocab)/num_files)
total_sents = total_sents/num_files

print("Overall Avgs: " + "Word Length: " + str(total_chars/total_words) + " Vocab: " + " Sentence Length: " + str(total_words/total_sents))
print(" ")