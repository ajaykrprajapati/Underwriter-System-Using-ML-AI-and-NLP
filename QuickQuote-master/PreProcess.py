# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import config
import logging

logger = logging.getLogger('QQ')


def changeFace(ans):
	ans = str(ans)
	val = re.sub("Face Amount: ", ' ', ans)
	val = re.sub(",", ' ', val)
	val = str(re.sub(" ", '', val))
	index = (val.find('$'))
	if(index != -1):
		val = val[1:]

	#val = int(val)
	return (val)


def changeWt(ans):
	ans = str(ans)
	val = re.sub("#", 'lb', ans)
	val = re.sub("lbs", 'lb', val)
	val = re.sub("Pounds", 'lb', val)
	val = re.sub("pounds", 'lb', val)
	val = str(re.sub(" ", '', val))
	if(re.search('KG|Kg|kg', val, re.I | re.U)):
		x = re.findall(r'\d+', ans)
		val = str(int(int(x[0]) * 2.2)) + 'lb'
	#val = int(val)
	return (val)

def changeHeight(ans):
	ans = str(ans)
	val = re.sub("Feet", '.', ans)
	val = str(re.sub(" ", '', val))
	if(re.search('inches|Inches', val, re.I | re.U) or val=='nan'):
		val = re.sub("Inches", '', val)
		return (val)
	else:
		val = re.sub("Inches", '', val)	
		val = re.sub("Inch", '', val)	
		val = val + '0'
		return (val)

def changePT(ans):
	ans = str(ans)
	val = re.sub("Product Type", '', ans)
	val = re.sub(":", '', val)
	val = str(re.sub(" ", '', val))
	return (val)

def emailfirst(doc):
	if(type(doc) == str):
		mails = doc.split(";")
		return str(mails[0])
	else:
		doc = ""
		return doc
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def standardize_famnt(doc):
	if(doc.isdigit()):
		number = int(doc)
		num = human_format(number)
		return(num)
	else:
		return(doc)

def preprocess_main(file):

	logger.info(">> Start - Preprocessing. Standardize Face amount, Weight... etc")
	logger.debug("Opening -" + config.regex_processed_csv)
	df = pd.read_csv(config.regex_processed_csv, encoding='UTF-8')
	df = df.drop(columns=['Year_of_Birth'])
	of = pd.read_csv(file, encoding='UTF-8')
	of['recepientemail'] = of['recepientemail'].apply(emailfirst)
	df['recepientemail'] = of['recepientemail'].values

	logger.info("Standardize Weight")
	df['Weight'] = df['Weight'].apply(changeWt)

	logger.info("Standardize Height")
	df['Height'] = df['Height'].apply(changeHeight)

	logger.info("Standardize Face amount")
	df['Face Amount'] = df['Face Amount'].apply(changeFace)
	
	logger.info("Standardize Product Type")
	df['Product Type'] = df['Product Type'].apply(changePT)
	df['Face Amount'] = df['Face Amount'].apply(standardize_famnt)
	# print(df['Face Amount'])

	
	#print(df)
	df.to_csv(config.preprocessed_csv, index=False, encoding="utf-8")
	logger.info("<< End - Preprocess")

preprocess_main(config.raw_data_csv)
