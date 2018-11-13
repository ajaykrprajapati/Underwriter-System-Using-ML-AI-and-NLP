# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
import logging
import config

logger = logging.getLogger('QQ')


def login():
	logger.info('Connect to mailbox - ' + EMAIL)
	server = IMAPClient(config.imap_server, use_uid=True, ssl=True)
	server.login(EMAIL, PASSWORD)
	logger.debug('Connection Established')
	return server
