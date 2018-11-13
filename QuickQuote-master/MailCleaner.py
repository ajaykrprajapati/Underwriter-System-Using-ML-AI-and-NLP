import EFZP as zp
import pandas as pd
import config
import logging

logger = logging.getLogger('QQ')


def mail_cleaner_main(file):
	logger.info(
		'>> Start - Mail Cleaning - Remove signature, Offer Standardize etc')

	df = pd.read_csv(file, encoding='utf-8')
	df['Contents'] = df['Contents'].apply(functionalZone)
	# df['Offer'] = df['Offer'].apply('rem_punct')
	# df['Offer_noise_free'] = apply.('Standardize')
	df.to_csv(file, index=False, encoding="utf-8")
	logger.info('<< End - Mail Cleaning')


def functionalZone(doc):
	p = zp.parse(doc)
	ans = " "

	if (str(p['body']) is not None):
		ans = ans + str(p['body'])
	if(str(p['reply_text']) is not None):
		ans = ans + str(p['reply_text'])
	return ans

# mail_cleaner_main(config.eraw_data_csv)
