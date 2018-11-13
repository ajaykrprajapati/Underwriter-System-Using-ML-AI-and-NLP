# -*- coding: utf-8 -*-

from imapclient import IMAPClient
from secrets import EMAIL, PASSWORD
from email import message_from_string
from email.message import EmailMessage
from email.headerregistry import Address
from MailLogin import login
import lxml.html
import re
import os
import pandas as pd
import collections
import config
import logging

logger = logging.getLogger('QQ')

def clean(data):
    # employing the lxml parser to clean the content of mail
    # every other thing is pretty self explanatory
    doc = lxml.html.document_fromstring(data)
    newdata = doc.text_content().encode('utf8').decode('utf8').strip()
    newdata = re.sub(r'<!--.+?-->', '', newdata,flags= re.DOTALL)
    return newdata.strip()


def get_decoded_email_body(message_body):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """
    msg = message_from_string(message_body)

    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():
            #logger.debug( "%s, %s" % (part.get_content_type(), part.get_content_charset()))
            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded
                # "something"
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == 'text/plain':
                text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

            if part.get_content_type() == 'text/html':
                html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

        if text is not None:
            return text.strip()
        else:
            return html.strip()
    else:
        text = str(msg.get_payload(decode=True),msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        return text.strip()


def write_to_csv(filename, data_dict):
    file_exists = os.path.isfile(filename)
    ordered_dict = [collections.OrderedDict(x) for x in data_dict]
    df = pd.DataFrame(ordered_dict)
    df.to_csv(filename, header=True, index=False, encoding='utf-8')


def filter_predicted(server, unread):
    df = pd.read_csv(config.predicted_csv, encoding='utf-8')
    fetch = server.fetch(unread, ['ENVELOPE'])
    new_unread,unread_ids = [], []
    for msgid, data in fetch.items():
        envelope = data[b'ENVELOPE']
        message_id = envelope.message_id.decode('utf8')
        unread_ids.append(message_id)
        if len(df[df['MessageID'] == message_id]) == 0 :
        # if message_id not in df['MessageID']:
            new_unread.append(msgid)
    for i in df['MessageID']:
    	if i not in unread_ids:
    		# df.query('MessageID != ' + i, inplace = True)
            df = df[df.MessageID != i]
    df.to_csv(config.predicted_csv, header = True, index = False, encoding = 'utf-8')
    return new_unread

def mail_reader(folder, flags, new_flags):
    logger.info('>> Start - Reading Mailbox')
    server = login()
    # Selecting the inbox folder
    message_box = server.select_folder(folder)

    # Gives list of unread messages
    messages = server.search(flags)

    # Filter the already predicted unread emails
    logger.debug(f'UnRead eMails {messages}')
    
    messages = filter_predicted(server, messages)
    logger.debug(f'Urpredicted eMails {messages}')

    # get_flags method gives the flags(Unseen or Seen) for each message
    # logger.debug(server.get_flags(messages))

    # Get the id, msg_id, subject, date, sender_email, receiver_email, content
    # from email
    logger.debug('Fetching Email Data')    
    body = server.fetch(messages, ['ENVELOPE', 'RFC822'])
    data_dict = []
    for msgid, data in body.items():
        envelope = data[b'ENVELOPE']
        content_raw = data[b'RFC822'].decode('utf8')
        content = clean(get_decoded_email_body(content_raw).decode('utf8'))
        date = envelope.date
        message_id = envelope.message_id.decode('utf8')
        subject = envelope.subject.decode('utf8')
        from_ = str(envelope.from_[0])
        to = str(envelope.to[0])
        row = {'ID': msgid, 'MessageID': message_id, 'Subject': subject, 'Senderemail': from_,
               'recepientemail': to, 'SentOn': date, 'ReceivedOn': date, 'Offer_noise_free': None, 'Contents': content}
        data_dict.append(row)
        
    # Writing data to csv
    write_to_csv(config.eraw_data_csv, data_dict)

    # to set messages unseen to mark it seen use [b'\\Seen']
    server.set_flags(messages, new_flags)

    # messages = server.search(['ALL'])
    # logger.debug(server.get_flags(messages))
    server.logout()
    logger.debug('<< End - Mail read')
    
# For getting all unread emails from inbox
# mail_reader('INBOX',['SEEN'],[b'\\SEEN'])

# mail_reader('INBOX', ['UNSEEN'], [])

# For getting all emails from sentbox
# mail_reader('SENT',['ALL'])