import os
import sys
import nltk
from nltk.parse import stanford
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk import ne_chunk
import re



#print sentences

#text="\"I would like to work for XYZ.\" : Here the intent of the sentence is 'To work for', the entity that the intent is aimed at is 'XYZ' and the Subject of the intent is 'I'"
#text = "The Minister found herself in an unhappy situation when the House unprecedentedly voted her to continue to be in power. I am a good man."


#tokenize and tag the sentences using NLTK tokenizer and using NLTK chunker to build a syntax tree
def preprocess(text):

	tokenizer = RegexpTokenizer(r'\w+') 
	tokenized = tokenizer.tokenize(text)
	tagged = nltk.pos_tag(tokenized)

	t = ne_chunk(tagged, binary=True)
	
	return tagged, t


#Search the nouns using POS tags and print them
def print_nouns(tagged):
	nouns=[]
	for tag in tagged:
		#words with POS tags beginning with N are nouns
		if re.search(r'^N',tag[1]):
			nouns.append(tag[0])
	if not nouns:
		print "Nouns not found\n"
	else:
		print 'Nouns: '+str(', '.join(nouns))

#Search the verbs using POS tags and print them
def print_verbs(tagged):
	verbs=[]
	for tag in tagged:
		#words with POS tags beginning with V are verbs
		if re.search(r'^V',tag[1]):
			verbs.append(tag[0])
	if not verbs:
		print "Verbs not found\n"
	else:
		print 'Verbs: '+str(', '.join(verbs))

#Search the adjectives using POS tags and print them
def print_adj(tagged):
	adj=[]
	for tag in tagged:
		#words with POS tags beginning with J are adjectives
		if re.search(r'^J',tag[1]):
			adj.append(tag[0])
	if not adj:
		print "Adjectives not found\n"
	else:
		print 'Adjectives: '+str(', '.join(adj))
	return adj

#Using the stopwords for English provided by nltk corpus
def print_stopwords(tagged):
	stopword=[]
	sw=stopwords.words('english')
	for word in tagged:
		if word[0] in sw:
			stopword.append(word[0])
	if not stopword:
		print "Stopwords not found\n"
	else:
		print 'Stopwords: '+str(', '.join(stopword))

#Search the adverbs using POS tags and print them
def print_adverb(tagged):
	adverb=[]
	for tag in tagged:
		#words with POS tags beginning with RB are adverbs
		if re.search(r'^RB',tag[1]):		
			adverb.append(tag[0])
	if not adverb:
		print "Adverbs not found\n"
	else:
		print 'Adverbs: '+str(', '.join(adverb))

#Using the synonyms provided in the NLTK corpus wordnet
def print_syn(adj):
	for word in adj:
		ls = wordnet.synsets(str(word),pos=wordnet.ADJ)
		lt=[]
		ant=[]
		for l in ls:
			lt.append(str(l.lemma_names()[0]))
		lts=list(set(lt))
		print 'Synonyms of '+str(word)+' are: '+str(', '.join(lts))
		
#Using the antonyms provided in the NLTK corpus wordnet
def print_ant(adj):
	for word in adj:
		ls = wordnet.synsets(word,pos=wordnet.ADJ)[0]
		ant=[]
		for i in ls.lemmas()[0].antonyms():
			ant.append(str(i.name()))
		print 'Antonyms of '+str(word)+' are: '+str(', '.join(ant))


#
def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label():
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    return entity_names
  
#Using StanfordDependencyParser to parse the text and using the  
def find_intent(text):

	os.environ["JAVAHOME"]="C:/Program Files/Java/jre1.8.0_141/bin"

	parser = stanford.StanfordDependencyParser('./stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0.jar','./stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0-models.jar','englishPCFG.ser.gz')

	for parse in parser.raw_parse(text):
		root = parse.root
		words = []
		if root['tag'].startswith("V"):
			words.append((root['word'], root['address']))

			for dep in root['deps']:
				#print dep
				if dep == 'xcomp' or dep == 'aux':
					token_ids = root['deps'][dep]
					for tokid in token_ids:
						node = parse.nodes[tokid]
						if node['tag'].startswith("V"):
							words.append((node['word'], node['address']))
							for ndep in node['deps']:
								if ndep == 'mark':
									nodetoken_ids = node['deps'][ndep]
									for ntokid in nodetoken_ids:
										auxnode = parse.nodes[ntokid]
										words.append((auxnode['word'], auxnode['address']))
				

		if len(words):
			word_zip = sorted(words, key=lambda x:x[1])
			words = zip(*word_zip)[0]
			print "The intent of the sentence is: \""+" ".join(words),"\""
		else:
			print "Could not find any intent!"

def main():

	filename = 'input1.txt'

	file = open(filename, 'r')

	lines=[line.strip() for line in file.readlines()]

	input_text = ' '.join(lines)

	sentences = sent_tokenize(input_text)


	i=1
	for text in sentences:

		print "*************************************************************\nFor sentence %d" % (i)
		#print text
		i+=1
		tagged, t = preprocess(text)
		print_nouns(tagged)
		print_verbs(tagged)
		print_stopwords(tagged)
		adj=print_adj(tagged)
		print_adverb(tagged)
		print_syn(adj)
		print_ant(adj)
		entity_names=extract_entity_names(t)
		if not entity_names:
			print "No entity found\n"
		else:
			print "Entities = " + str(entity_names)
		find_intent(text)

if __name__ == "__main__":
	main()
