# -*- coding: utf-8 -*-

import pandas as pd
import re
import config
from datetime import datetime
import logging
'''
try:
	from search_term import give_med_terms
except:
	from QuickUMLS.search_term import give_med_terms
'''

logger = logging.getLogger('QQ')

number = r'\d{2,3}'

gender = r'(\b[Mm]ale?)|(\b[Ff]emale?)|(\bFEMALE)|(\bMALE)|(\bF/\s?(age)?\s?\d{2,3})|(\bM/\s?(age)?\s?\d{2,3})|(\bf/\s?(age)?\s?\d{2,3})|(\bm/\s?(age)?\s?\d{2,3})'

Date = r'(([A-Z0-9][A-Z0-9]?[/-])?[A-Z0-9][A-Z0-9]?[/-][A-Z0-9][A-Z0-9][A-Z0-9]?[A-Z0-9]?)|([A-Za-z][A-Za-z][A-Za-z]\s..?[,]\s....)'

DOB  = r'(.*)?DOB|[Dd][aA][tT][eE]\s[oO][fF]\s[Bb][iI][rR][tT][hH]\s?(.*)?'

year_four_digit = r'\b(19|20)\d{2}(w+)?'
year_two_digit = r'\d{2}$(w+)?'

product_type = r'(\b[Pp]roduct\s[Tt]ype):\s?.*'
permanent = r'[Pp][eE][rR][mM]([aA][nN][aA][nN][tT])?'
term = r'\b[tT][eE][rR][mM]\b'

#Assuming USA currency dollar
amount_with_dollar = r'(\$\s?\d{1,3}(,\d{2,3})*(\.\d+)?)(\s?[kK]?)(\s?[mM]?[mM]?(illion)?(ILLION)?)([bB]?)'
amount_without_dollar = r'(\$?\s?\d{1,3}(,\d{2,3})*(\.\d+)?)(\s?[kK]?)(\s[mM]?[mM]?(illion)?(ILLION)?)([bB]?)((\s?[Yy][Ee][aA][rR][sS]?)?)'
faceamount = r'(\b([Ff]ace\s?)?[Aa]mount:?\s?.*)'
termamount = r'((.*)?[Tt][eE][rR][mM](.*)?)|((.*)?[pP][eE][rR][mM](.*)?)'   	#Regex to read single line from first newline to next newline
seeking = r'(.*)?[Ss][eE][eE][kK]([iI][nN][gG])?(.*)?'
cover = r'(.*)?[Cc][oO][vV][eE][rR]([aA][gG][eE])?(.*)?'
term_year = r'(y(ea)?r|Y(ea)?r|Y(ea)?r)'
k_conv = r'(\s?[kK])'
m_conv = r'(\s?[mM][mM]?(illion)?(ILLION)?)'
num_conv = r'\d{1,3}'
ul = r'(.*)?[uU][lL](.*)?'
ul_with_dollar = r'(\$\s?\d{1,3}(,\d{2,3})*(\.\d+)?)'
ul_without_dollar = r'(\$?\s?\d{1,3}(,\d{2,3})*(\.\d+)?)'


weight = r'(.*)?\b[wW][eE][iI][gG][hH][tT]\s?(.*)?' 
weight_num = r'(\d*\.?\d+)\s?(lb|lbs|Lbs|LB|LBS|kg|Kg|KG|#|Pounds|pounds)'		#r'(.*)\s?([lL][bB][sS]|[oO][zZ]|[gG]|[kK][Gg])' 

age_only = r'\b([Aa][Gg][Ee])\b'
age_simple = r'(.*)?[Aa][Gg][Ee]\s?(.*)?'
age = r'(.*\s?[Yy]([eE][aA])?[rR]?[sS]?\s?([oO][lL][dD])?)'
age_from_gender = r'(.*)?(\b[Mm]ale?)|(\b[Ff]emale?)|(\bFEMALE)|(\bMALE)|(\b)\s?(.*)?' 

height_num = r'\d{1,2}'
height1 = r'((.*)?\s?([Ff][eE][eE][tT])((.*)?\s?([iI][nN][Cc][Hh]([Ee][Ss])?))?)'			#Two types of inches => "|”
height2 = r'.[\'](\s?.[\"|\'\'])?' 											
feet = r'\d[\']'
inches = r'\d[\"|\'\']' 

preferred = r'(.*)?(Preferred|preferred)\s?(.*)?'
height_word = r'Height|height'
weight_word = r'Weight|weight' 

build = r'(Build|build)\s?(.*)?'
build_weight = r'\d{3}'
build_height = r'\d\.\d'

smoker = r'(.*)?[sS][Mm][oO][Kk]([eE][rR])?\s?(.*)?' 
tobacco = r'(.*)?[Tt][oO][bB][aA][cC][cC][oO]\s?(.*)?'
no = r'[nN][oO]'
never = r'\b[nN][eE][vV][eE][rR]\b'

med = r'(.*)?\b[mM][eE][dD][iI][cC][aA][tT][iI][oO][nN]\s?(.*)?'

family = r'(.*)?(\b[Ff]amily)\s?(.*)?'
family_member = r'(.*)?(\b[Mm]om)\s?(.*)?|(.*)?(\b[Mm]other)\s?(.*)?|(\b[Ff]ather)\s?(.*)?|(\b[Dd]ad)\s?(.*)?|(\b[Ss]ister)\s?(.*)?|(\b[Bb]rother)\s?(.*)?|(\b[Hh]usband)\s?(.*)?|(\b[Ww]ife)\s?(.*)?|(\b[Pp]aternal)\s?(.*)?|(\b[Mm]aternal)\s?(.*)?|(\b[Gg]randfather)\s?(.*)?|(\b[Gg]randmother)\s?(.*)?|(\b[Ff]amily)\s?(.*)?'

lives = r'(.*)?(\b[Ll]ives)\s?(.*)?'
prop = r'(.*)?(\b[Pp]roperty)\s?(.*)?'

#age_slash =""

def genderRegex(line):	
	ans=""
	#for line in st:
	male_with_age = r'\b[Mm]/\s?(age)?\s?\d{2,3}'
	female_with_age = r'\b[Ff]/\s?(age)?\s?\d{2,3}'
	y = re.search(gender, line, re.I | re.U)
	if(y):
		y_male_age = re.search(male_with_age, y.group(0), re.I | re.U)
		y_female_age = re.search(female_with_age, y.group(0), re.I | re.U)
		
		if(y.group(0)=='F/' or y.group(0)=='f/' or y.group(0)=='f/age'):
			ans='Female'
			#age_slash_reg = re.search(number, y.group(0), re.I | re.U)
			#age_slash=age_slash_reg.group(0)
			
		elif(y.group(0)=='M/' or y.group(0)=='m/' or y.group(0)=='m/age'):
			ans='Male'
			#age_slash_reg = re.search(number, y.group(0), re.I | re.U)
			#age_slash=age_slash_reg.group(0)
			
		elif(y_male_age):
			ans='Male'
			#age_slash_reg = re.search(number, y_male_age.group(0), re.I | re.U)
			#age_slash=age_slash_reg.group(0)
		
		elif(y_female_age):
			ans='Female'	
			#age_slash_reg = re.search(number, y_female_age.group(0), re.I | re.U)
			#age_slash=age_slash_reg.group(0)
			
			
		else:
			#print (y.group(0)+"\n")
			ans=(y.group(0))
			age_slash=""
	elif(y and num):
		ans=(y.group(0))
	else:
		ans=""
	
	logger.debug("Gender= " + ans.strip().lower())
	return ans.strip().lower()

def yearRegex(line):
	ans=""
	num = re.search(number, line, re.I | re.U)
	x = re.search(Date, line, re.I | re.U)
	ans = 0
	z = 0
	x1 = re.search(year_four_digit, line, re.I | re.U)
	if(x):
		x1 = re.search(year_four_digit, x.group(0), re.I | re.U)
		x2 = re.search(year_two_digit, x.group(0), re.I | re.U)				
		if(x1):
			ans=x1.group(0)
		elif(x2):
			z = x2.group(0)									
			#print('Last 2 digits of Year of birth='+z)
			ans= '19'+str(z)
	elif(x1):
		x1 = re.search(year_four_digit, line, re.I | re.U)
		#print (x1.group(0))
		ans=x1.group(0)
	else:
		ans=""
		
	logger.debug("Year= " + str(ans))	
	return ans

def productRegex(line):
	ans=""
	z=re.search(product_type, line, re.I | re.U)
	perm_reg = re.search(permanent, line, re.I | re.U)
	term_type_reg = re.search(term, line, re.I | re.U)
	if(z): 
		#print (z.group(0)+"\n")
		ans=(z.group(0))
	elif(perm_reg):
		final_str = "Product Type: Permanent"
		ans=(final_str)
	elif(term_type_reg):
		final_str= "Product Type: Term"
		ans=(final_str)
	else:
		ans=""
	
	logger.debug("Product= " + ans.strip())
	return ans.strip()

def weightRegex(line):
	ans=""
	#Preferred Height & Weight
	pr = ''
	pr = re.search(preferred, line, re.I | re.U)
	if(pr!='' and pr):
		w_reg = re.search(weight_word, pr.group(0), re.I | re.U)
		if(w_reg):
			ans = "196 lbs"
			return ans.strip()
	else:
		x=re.search(weight_num, line, re.I | re.U) 
		wt=re.search(weight, line, re.I | re.U)
		if(x): 
			#print (x.group(0)+"\n")
			ans=(x.group(0))
		elif(wt):
			am = re.search(weight_num,wt.group(0), re.I | re.U)
			if(am):
				ans=(am.group(0))
		else:
			ans=""

	logger.debug("Weight= " + ans.strip())	
	return ans.strip()

def heightRegex(line):
	ans=""
	#Preferred Height & Weight
	pr = ''
	pr = re.search(preferred, line, re.I | re.U)
	if(pr!='' and pr):
		h_reg = re.search(height_word, pr.group(0), re.I | re.U)
		if(h_reg):
			ans = "5 Feet 9 Inches"
			return ans.strip()
	else:
		ht = re.search(height1, line, re.I | re.U)
		htsym = re.search(height2, line, re.I | re.U)
		if(ht): 
			#print (ht.group(0)+"\n")
			ans=(ht.group(0))
		elif(htsym):
			f = re.search(feet, (htsym.group(0)), re.I | re.U)
			inch = re.search(inches, (htsym.group(0)), re.I | re.U)
			if(f):
				#print(f.group(0))
				am = re.search(height_num, (f.group(0)), re.I | re.U).group(0) + ' Feet '
				if(inch):
					am+=(re.search(height_num, (inch.group(0)), re.I | re.U).group(0)) + ' Inches' 
				ans=am
		else:
			ans=""

	logger.debug("Height= " + ans.strip())
	return ans.strip()

def ageRegex(line):
	
	age_reg = re.search(age, line, re.I | re.U)
	age_simple_reg = re.search(age_simple, line, re.I | re.U)
	dob = re.search(DOB, line, re.I | re.U)
	age_gender_reg = re.search(age_from_gender, line, re.I | re.U)
	x1 = re.search(year_four_digit, line, re.I | re.U)
	
	if(age_gender_reg):										#Male 20
			am = re.search(number, age_gender_reg.group(0), re.I | re.U)
			if(am):
				ans=am.group(0)
	
		
	if(x1):													#20/03/1996
		#print ("DOB:"+x1.group(0))
		currentYear = datetime.now().year
		#print (currentYear-(int)(x1.group(0)))
		ans=((currentYear-(int)(x1.group(0))))
	
	else:
		if(x1 and dob):										#DOB 20/03/1996
			#print ("DOB:"+x1.group(0))
			currentYear = datetime.now().year
			#print (currentYear-(int)(x1.group(0)))
			ans=((currentYear-(int)(x1.group(0))))
		elif(x1 and y):										#Male 20/03/1996
			#print ("DOB:"+x1.group(0))
			currentYear = datetime.now().year
			#print (currentYear-(int)(x1.group(0)))
			ans=((currentYear-(int)(x1.group(0))))
		else:
			ans=' '
			
		if(age_reg):										#20 years ago
			age_num = age_reg.group(0)			
			an = re.search(number, age_num, re.I | re.U)
			if(an):				
				
				#print ("DOB:"+ an.group(0))
				ans=(an.group(0))
	
		
		ans_year = yearRegex(line)							#With Year of birth 
		#print(type(ans_year), ans_year)	
		
		if(ans_year and ans_year!=0):
			currentYear = datetime.now().year
			ans=(currentYear-(int)(ans_year))
		
		if(age_simple_reg):									#Age 20
			age_only_reg = re.search(age_only, age_simple_reg.group(0), re.I | re.U)
			if(age_only_reg):
				age_num = age_simple_reg.group(0)			
				an = re.search(number, age_num, re.I | re.U)
				if(an):				
					#print ("DOB:"+ an.group(0))
					ans=(an.group(0))
					
	#if(age_slash!=""):
	#	ans='30'
	
	logger.debug("Age= " + str(ans))
	return ans

def habitRegex(line):
	ans=""
	sm = re.search(smoker, line, re.I | re.U)
	tob = re.search(tobacco, line, re.I | re.U)
	if(sm): 
		if(re.search(no, sm.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		elif(re.search(never, sm.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		else:
			ans="Tobacco"
	elif(tob):
		#print(tob.group(0))
		if(re.search(no, tob.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		elif(re.search(never, tob.group(0), re.I | re.U)):
			ans="Non-Tobacco"
		else:
			ans="Tobacco"
	else:
		ans=""
		
	logger.debug("Habit= " + ans.strip())	
	return ans.strip()
	
def faceamountRegex(line):
	ans=""
	w = re.search(faceamount, line	, re.I | re.U)
	term_reg = re.search(termamount, line, re.I | re.U)
	seek_reg = re.search(seeking, line, re.I | re.U)
	coverage_reg = re.search(cover, line, re.I | re.U)
	ul_reg = re.search(ul, line, re.I | re.U)
	#With faceAmount
	if(w):
		k = re.search(k_conv, w.group(0), re.I | re.U)
		if(k):
			nn = re.search(num_conv, w.group(0), re.I | re.U)
			ans='Face Amount: $'+((nn.group(0))+',000')
		else:
			ans=(w.group(0))

	#With term Amount
	elif(term_reg):
		amd = re.search(amount_with_dollar, term_reg.group(0), re.I | re.U)
		amwd = re.search(amount_without_dollar, term_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		z = 0
		if(amd):
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)
	#With Seeking
	elif(seek_reg):
		amd = re.search(amount_with_dollar, seek_reg.group(0), re.I | re.U)
		amwd = re.search(amount_without_dollar, seek_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		if(amd):
			#ans='Face Amount: '+(amd.group(0))
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)
	#With Coverage
	elif(coverage_reg):
		amd = re.search(amount_with_dollar, coverage_reg.group(0), re.I | re.U)
		amwd = re.search(amount_without_dollar, coverage_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		if(amd):
			#ans='Face Amount: '+(amd.group(0))
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)
		
	#with ul
	elif(ul_reg):
		amd = re.search(ul_with_dollar, ul_reg.group(0), re.I | re.U)
		amwd = re.search(ul_without_dollar, ul_reg.group(0), re.I | re.U)			#Find 2nd regex in the same line of 1st regex 
		z = 0
		if(amd):
			k = re.search(k_conv, amd.group(0), re.I | re.U)
			m = re.search(m_conv, amd.group(0), re.I | re.U)
			if(k):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000')
			elif(m):
				nn = re.search(num_conv, amd.group(0), re.I | re.U)
				ans='Face Amount: '+((nn.group(0))+',000,000')
			else:
				ans='Face Amount: '+amd.group(0)
		elif(amwd):
			term_year_reg = re.search(term_year, amwd.group(0), re.I | re.U)
			if(term_year_reg):
				ans='Term Year: '+(amwd.group(0))
			else:
				#ans='Face Amount: $'+(amwd.group(0))
				k = re.search(k_conv, amwd.group(0), re.I | re.U)
				m = re.search(m_conv, amwd.group(0), re.I | re.U)
				if(k):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000')
				elif(m):
					nn = re.search(num_conv, amwd.group(0), re.I | re.U)
					ans='Face Amount: $'+((nn.group(0))+',000,000')
				else:
					ans='Face Amount: $'+amwd.group(0)

	else:
		ans=""
	
	logger.debug("Face Amount= " + ans.strip())
	return ans.strip()
	
def medicationRegex(line):
	#Medication & Treatment
	ans=""
	med_reg = (re.search(med,line, re.I | re.U))
	ans = ""
	if(med_reg):
		if(re.search(no, med_reg.group(0), re.I | re.U)):
			ans="No Medication"
	else:
		ans = " "
	
	logger.debug("Medication= " + ans.strip())
	return ans.strip()

def propertyRegex(line):
	#Property
	ans =""
	lives_reg = (re.search(lives,line, re.I | re.U))
	prop_reg = (re.search(prop,line, re.I | re.U))
	if(lives_reg):
		ans=lives_reg.groups()
		if(prop_reg):
			ans=lives_reg.groups()+prop_reg.groups()
	elif(prop_reg):
		ans=prop_reg.groups()
	
	logger.debug("Property= " + str(ans))
	return ans

def familyRegex(line):
	#Family
	ans=""
	family_reg = (re.search(family,line, re.I | re.U))
	family_member_reg = (re.search(family_member,line, re.I | re.U))
	if(family_reg):
		ans=family_reg.groups()
	elif(family_member_reg):
		ans=family_member_reg.groups()
	else:															#Write else outsite condition (to stop rewriting of above cell)
		ans=""
	
	logger.debug("Family= " + str(ans))
	return ans


def medicalTerms(doc):
	ans = set(['med terms','cancer','tb'])
	# ans = give_med_terms(doc)
	logger.debug(f"Medical Terms={ans}")
	return ans

def regexmain(file):
	logger.info(">> Start - Feature Extraction - RegEx")
	
	df = pd.read_csv(file, encoding='UTF-8')
	of = pd.DataFrame()
	
	of['Contents'] = df['Contents']
	of['Offer_noise_free'] = df['Offer_noise_free']
	of['recepientemail'] = df['recepientemail']
	
	logger.info("Feature Extraction - Gender")
	of['Gender'] = of['Contents'].apply(genderRegex)
	
	logger.info("Feature Extraction - DOB")
	of['Year_of_Birth'] = of['Contents'].apply(yearRegex)
	
	logger.info("Feature Extraction - Age")
	of['Age(years)'] = of['Contents'].apply(ageRegex)
	
	logger.info("Feature Extraction - Product Type")
	of['Product Type'] = of['Contents'].apply(productRegex)
	
	logger.info("Feature Extraction - Weight")
	of['Weight'] = of['Contents'].apply(weightRegex)
	
	logger.info("Feature Extraction - Height")
	of['Height'] = of['Contents'].apply(heightRegex)
	
	logger.info("Feature Extraction - Habit")
	of['Habit'] = of['Contents'].apply(habitRegex)
	
	logger.info("Feature Extraction - Face Amount")
	of['Face Amount'] = of['Contents'].apply(faceamountRegex)
	
	logger.info("Feature Extraction - Medication")
	of['Medication'] = of['Contents'].apply(medicationRegex)
	
	logger.info("Feature Extraction - Property")
	of['Property'] = of['Contents'].apply(propertyRegex)
	
	logger.info("Feature Extraction - Medical Terms - UMLS")
	of['Medical Data'] = of['Contents'].apply(medicalTerms)
	
	logger.info("Feature Extraction - Family History")
	of['Family'] = of['Contents'].apply(familyRegex)
	
	# df = df.drop(columns=['Contents'])	
	of.to_csv(config.regex_processed_csv,index =False, encoding='utf-8')
	
	logger.info("<< End - Feature Extraction - RegEx")
	
#regexmain(config.raw_data_csv)	





