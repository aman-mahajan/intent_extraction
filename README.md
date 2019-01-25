# Intent Extraction

The objective of this Python script is to do the following:
Read a text file, split the input text content into sentences and then for each sentence print the following features.
1. All the nouns in the Sentence.
2. All the verbs in the sentence.
3. All the stop words that appear in the sentence
4. All the adjectives in the sentence
5. All the adverbs in the sentence
6. All the synonyms for every adjective of the sentence.
7. Antonym of every adjective in the sentence.
8. All the entities in the sentence.
9. Find the intent of the sentence – (Ex: “I would like to work for XYZ” : Here the intent of the sentence is ‘To work for’, the entity that the intent is aimed at is ‘XYZ’ and the Subject of the intent is ‘I’)


### Explanation and Reasoning behind the approach

If we divide the sentence into subject-verb-object clauses, the verb phrase will be the intent of the sentence. To extract the verb phrase, the following is done:
1.	Using a dependency parser, find the dependency parse tree. 
2.	The root of the parse tree is usually a verb in simple sentences.
For example, Given “She asked George to respond to the offer”, the dependency parser gives “asked” as the root.
3.	“asked” and “respond” are two verbs connected in the parse tree using the relation “xcomp”. That is “respond” is an open clausal complement of “asked”. I took into account only verb-verb xcomp relationships. Thus given the root verb, I find the verbs connected to it by xcomp
4.	Post that I look at words connected to these verbs via either “aux” and “mark” relationships to capture auxiliary words like “will”, “would”, “should” etc.
5.	Sorting these list of words gives the intent.

### Pros:
*	It works reasonably well in simple declarative sentences.

### Cons:
*	Would not be able capture multiple intents in a single sentence, since we start at the root and capture related words. 
*	For example: I like to work for XYZ and perform well. Here only “like to work” will be captured. 
*	May capture some words not needed to intent, as part of aux or marker
*	May not work for sentences in passive voice and sentences without proper subject-verb-object mentioned. 
