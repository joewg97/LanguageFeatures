import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize, ngrams
import os, sys, re, io, codecs

#nltk.download("gutenberg")


def languageFeatures(filename):
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
	sents = nltk.sent_tokenize(raw)
	chars = [c.lower() for c in raw]

	num_chars = len(chars)
	num_words = len(words)
	num_vocab = len(set(words))
	num_sents = len(sents)

	awl = round(num_chars/num_words)
	asl = round(num_words/num_sents)
	lexdiv = round(num_words/num_vocab)
	spellvar = 0
	
	for w in set(words):
		if not wordnet.synsets(w):
			spellvar = spellvar + 1
	
	print("File: " + filename)
	print("Avg. Word Length: ", awl, "Avg. Sentence Length: ", asl, "Lexical Diversity: ", lexdiv, "Spelling Variation: ", spellvar/num_vocab)

	print("Word Frequency: ")
	vocab = set(words)
	vocab_size = len(vocab)
	fdist = nltk.FreqDist(words)
	for x,y in fdist.most_common(vocab_size):
		print(x.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding, errors='replace'),y)
	print(" ")

	print("Character Ngram Frequency: ")
	ngram = nltk.FreqDist(vs for word in words
		for vs in re.findall(r'[abcdefghijklmnopqrstuvwxyz]{3}', word))
	for k,v in ngram.most_common():
		print (k,v)
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

for filename in os.listdir("C:/Users/joewg/Documents/TYP/EEBO texts/EEBO texts/split-plase1/split/CERTAIN/1700-1724"):
    if filename.endswith(".xml"): 
        languageFeatures(filename)
        continue
    else:
        continue