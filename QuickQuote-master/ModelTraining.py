# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import config
from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import wordpunct_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
import pickle
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
#from xgboost.sklearn import XGBClassifier
import time
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from DataRepresentation import visualize
import logging

logger = logging.getLogger('QQ')

# Removes all punctuations which acts as noise


def rem_punt(doc):
	ans = re.sub('"|\\n|\(|\)|\.|[$!--+#:]{}', ' ', doc)
	ans = re.sub(' +', ' ', ans)
	ans = ans.lower()
	return ans

# Stop words removal using tokenization


def tokenize(document):
	lemmy = []
	stop_word = set(stopwords.words('english'))
	for sent in sent_tokenize(document):
		for token, tag in pos_tag(wordpunct_tokenize(sent)):
			# print(token,tag)
			if token in stop_word:
				continue
			lemma = lemmatize(token, tag)
			lemmy.append(lemma)
	return lemmy

# Lemmatization for tokens simplification


def lemmatize(token, tag):
	tag = {
		'N': wn.NOUN,
		'V': wn.VERB,
		'R': wn.ADV,
		'J': wn.ADJ
	}.get(tag[0], wn.NOUN)
	lemmatizer = WordNetLemmatizer()
	return lemmatizer.lemmatize(token, tag)


def model_saving(model_name, model):
	filename = config.raw_data_type + model_name + '.sav'
	pickle.dump(model, open('SavedModels/' + filename, 'wb'))


def model_making(model_name, vect, model, X_train, y_train, X_test, y_test):
	logger.info(f">> Start - Model training {str(model_name)}")
	t1 = time.time()

	clf = make_pipeline(vect, model)
	clf.fit(X_train, y_train)

	t2 = time.time()
	training_time = (t2 - t1)

	model_saving(model_name, clf)
	t1 = time.time()

	pd = clf.predict(X_test)
	t2 = time.time()
	prediction_time = (t2 - t1)

	y_pred = clf.predict(X_test)

	results = (accuracy_score(y_test, y_pred) * 100)
	logger.info("{:20} {:^20.3f} {:^20.3f} {:20.3f}s \n ".format(model_name, results, training_time, prediction_time))
	logger.info(f"{confusion_matrix(y_test, y_pred)}")


def conversion(doc):
	return(str(doc))

def model_with_SVD(vectorizer,X_train,X_test,y_train,y_test):
	svd = TruncatedSVD(n_components = 10,n_iter=7, random_state=42)
	lsa = make_pipeline(vectorizer,svd, Normalizer(copy=False))
	clf = ExtraTreesClassifier(n_estimators=200,n_jobs=-1,max_depth=36)
	pipe = make_pipeline(lsa, clf)
	pipe.fit(X_train,y_train)
	y_pred = clf.predict(X_test)
	results = (accuracy_score(y_test, y_pred) * 100)
	print("Results: ",results)


def model_making_main(file):
	logger.info(">> Start - Model making")

	df = pd.read_csv(config.preprocessed_csv, encoding='UTF-8')
	# If getting an error remove .astype(str)
	select_columns = ['recepientemail','Gender','Age(years)','Product Type','Weight','Height','Habit','Face Amount','Medication','Property','Medical Data','Family']
	df['ColumnA'] = df[select_columns].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)

	logging.info("Remove puncutation, tokenize")
	df['Lemmitize'] = df['ColumnA'].apply(rem_punt).apply(tokenize)

	df['Lemmitize'] = df['Lemmitize'].apply(conversion)
	df.to_csv(config.nlp_processed_csv, index=False, encoding="utf-8")

	df = pd.read_csv(config.nlp_processed_csv)

	X = df['Lemmitize']
	of = pd.read_csv(file, encoding='UTF-8')
	y = of['Offer_noise_free']

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
	vect = TfidfVectorizer(max_df=0.5, max_features=10000,min_df=1, use_idf=True, ngram_range=(1, 2), lowercase=True)
	represent = TfidfVectorizer(max_df=0.5, max_features=10000,min_df=1, use_idf=True, ngram_range=(1, 1), lowercase=True)
	matrix = represent.fit_transform(X.values)
	# visualize(represent,matrix,X,y)
	# print(matrix)

	# for i, feature in enumerate(vect.get_feature_names()):
	#    print(i, feature)

	#va = raw_input()

	#model1 = XGBClassifier(nthread=4,n_estimators=1000)
	model3 = RandomForestClassifier(n_estimators=60, n_jobs=3, max_features="auto", min_samples_leaf=50)
	model4 = SVC(kernel='rbf', C=1, gamma=10)
	model5 = LogisticRegression()
	model7 = SGDClassifier(alpha=.0001)
	model_making("XGBOOST",vect, model1, X_train, y_train, X_test, y_test)
	model_making("Random Forest", vect, model3,X_train, y_train, X_test, y_test)
	model_making("SVM", vect, model4, X_train, y_train, X_test, y_test)
	model_making("Logistic Regression", vect, model5,X_train, y_train, X_test, y_test)
	model_making("SGDClassifier", vect, model7,X_train, y_train, X_test, y_test)
	# model_with_SVD(vect,X_train,X_test,y_train,y_test)
	logger.info("<< End - Model making")


# model_making_main(config.raw_data_csv)
