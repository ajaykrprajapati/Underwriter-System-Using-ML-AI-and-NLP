# -*- coding: utf-8 -*-


from MailAutomation import mail_reader
from Prediction import prediction_main
from MailAppend import mail_append_main
import config
import os
import logging

# Log configuration and initialization
logger = logging.getLogger('QQ')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler = logging.FileHandler(config.log)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

def prediction_maker_main():
	logger.info(">> Start - Predection maker")

	mail_reader(config.email_box, config.email_flags, config.email_new_flags)
	if os.stat(config.eraw_data_csv).st_size <= 1:
		logging.warn("No UnRead/UnPredicted mails found.")
		return

	prediction_main(config.eraw_data_csv)
	mail_append_main()
	logger.info("<< End - Predection maker")

prediction_maker_main()
