# -*- coding: utf-8 -*-

from ModularRegex import regexmain
from PreProcess import preprocess_main
from ModelTraining import model_making_main
from MailCleaner import mail_cleaner_main
import config
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


def model_maker_main():
	logger.info('>> Start - Model Maker')

	mail_cleaner_main(config.raw_data_csv)

	regexmain(config.raw_data_csv)

	preprocess_main(config.raw_data_csv)

	model_making_main(config.raw_data_csv)

	logger.info('<< End - Model Maker')

model_maker_main()
