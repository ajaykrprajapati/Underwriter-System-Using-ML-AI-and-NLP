try:
	from QuickUMLS.quickumls import *
except:
	from quickumls import *
import os
import time
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.util import mark_negation

# text = '''
# subject: don-prostate
# $Xm plus perm

# XX/XX/51

# prostate cancer 4 Â½ years ago. treated. no recurrence. regular 6 month doctor visits.

# stage 3

# gleason is 3 +47

# radical prostatectomy

# no other health issues.

# '''


# def give_med_terms(text):
# 	dir_path = os.path.dirname(os.path.realpath(__file__))
# 	src = dir_path + '/quickumlsfiles/'
# 	matcher = QuickUMLS(src)
# 	result = matcher.match(text, best_match=True, ignore_syntax=False)
# 	set_terms = set()
# 	for i in result:
# 		for j in i:
# 			if j['similarity'] > 0.8:
# 				set_terms.add(j['ngram'])
# 	# for i in term:
# 	#	print(i)
# 	return set_terms

def term_filter(terms):
	with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/Data/filter.json','r',encoding = 'utf-8') as jfile:
		filter_dict = json.load(jfile)
	terms = set([term for term in terms if term not in filter_dict])
	return terms


def give_med_terms(text):
	dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	src = dir_path + '/quickumlsfiles/'
	matcher = QuickUMLS(src)
	txt = sent_tokenize(text)
	terms = set()
	for sentence in txt:
		result = matcher.match(sentence, best_match=True, ignore_syntax=False)
		set_terms = set()
		for i in result:
			for j in i:
				if j['similarity'] > 0.8:
					set_terms.add(j['ngram'])
		s_terms = term_filter(set_terms)
		new_terms = negation_check(sentence, s_terms)
		terms = terms.union(new_terms)
	return terms


def negation_check(sentence, set_terms):
	words = word_tokenize(sentence)
	negations = mark_negation(words)
	only_neg = list(set(negations).difference(words))
	if(len(only_neg) == 0):
		return set_terms
	only_neg = [x[:-4] for x in only_neg]
	terms = list(set_terms)
	for i, term in enumerate(terms):
		for t in term.split():
			if t in only_neg:
				terms[i]=term+'_NEG'
				break
	return set(terms) 

# print(give_med_terms(text))
