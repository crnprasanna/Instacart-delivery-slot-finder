#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
    User configuation module
	
Linux path - You can find by running command:
>>which chromedriver
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'

Windows path - Downloaded absolute path
CHROME_DRIVER_PATH = '<PATH_TO_CHROMEDRIVER_win32>\\chromedriver.exe'


Supported stores list:
1. 'lucky-supermarkets'
2. 'costco'
3. 'safeway'
4. 'target'
5. 'sprouts'
6. 'cvs'
7. 'bevmo'
8. 'sigonas-farmers-market'
9. 'rainbow-grocery'
10. 'smart-final'
11. 'petco'
12. 'total-wine-more'
13. 'raleys'
14. 'foodsco'
15. 'piazzas-fine-foods'

'''

CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'

STORE_LIST = ['costco']
INSTA_LOGIN_EMAIL = '<YOUR_INSTACART_LOGIN_ID>'
INSTA_LOGIN_PASS = '<YOUR_INSTACART_PASSWORD>'

SEND_GMAIL = True

# Needs below information, unless you set SEND_GMAIL flag to False
# Check readme for more information

SENDER_GMAIL_ID = '<YOUR_GMAIL_LOGIN_ID>'  # ex: test@gmail.com
SENDER_GMAIL_PASS = '<YOUR_GMAIL_PASSWORD>'  # Gmail app specific passwords or gmail login password
RECEIVER_EMAIL_ID = '<RECEIVER_EMAIL_ID>'  # Ex: test@hotmail.com
