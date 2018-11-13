# for outlook.com
imap_server = "imap-mail.outlook.com"
imap_port = 993
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
# if you choose this lib for office365.com, please comment above and uncomment below
#imap_server = "outlook.office365.com"
#imap_port = 993
#smtp_server = "smtp.office365.com"
#smtp_port = 587

# File paths
preprocessed_csv = 'Data/PProcessed.csv'
nlp_processed_csv = 'Data/NLPProcessed.csv'
raw_data_csv = 'Data/raw_data1.csv'
regex_processed_csv = 'Data/regexProcessed.csv'
eraw_data_csv = 'Data/eraw_data.csv'
enlp_processed_csv = 'Data/NLPProcessed.csv'
template = 'Data/email.template'
predicted_csv = 'Data/predicted.csv'
filter_json = 'Data/umls_filter.json'

# email
email_from = 'Trial waliid <trial_wali_id@outlook.com>'
email_box = 'INBOX'
email_new_flags = []
email_flags = ['UNSEEN']
append_box = 'Test'

# Logs
log = 'logs/QQ-logs.log'

# raw_data_type
raw_data_type = '1k_'
