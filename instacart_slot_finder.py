#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
	Instacart Slot finder - main module
'''

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import settings
from logger import Logger
import time
import smtplib
from email.mime.text import MIMEText
import timeout
from signal import signal, SIGINT
import sys
from datetime import datetime, timedelta
import timeout_decorator


class InstaSlotFinder:

	def __init__(self):
		self.url = 'https://www.instacart.com'
		self.store_url = \
			'https://www.instacart.com/store/costco/storefront'
		self.no_slot_msg = 'See delivery times'
		self.slots_dict = {}
		self.delivery_slot = []
		self.slots_result = ''
		self.browser = None
		self.server = None

		self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		self.supported_store_list = [
			'costco',
			'lucky-supermarkets',
			'safeway',
			'target',
			'sprouts',
			'cvs',
			'bevmo',
			'sigonas-farmers-market', 
			'rainbow-grocery',
			'smart-final',
			'petco',
			'total-wine-more',
			'raleys',
			'foodsco',
			'piazzas-fine-foods'
			]

		self.logger = Logger()
		signal(SIGINT, self.handler)

	def handler(self, signal_received, frame):

		# Handle any cleanup here

		msg = 'SIGINT or CTRL-C detected. Exiting gracefully'
		self.log_msg(msg)
		self.close_connection()

		sys.exit(0)

	@timeout.custom_decorator
	def start_browser(self):
		self.logger.log('\n##########################################')
		self.logger.log('Going to init browser')
		self.logger.log('Input Config:')
		self.logger.log('\tChrome driver path: {}'.format(
			settings.CHROME_DRIVER_PATH))
		self.logger.log('\tStores List: {}'.format(settings.STORE_LIST))
		self.logger.log('\tInstacart Login: {}'.format(
			settings.INSTA_LOGIN_EMAIL))
		self.logger.log('\tSEND_GMAIL report: {}'.format(
			settings.SEND_GMAIL))
		self.logger.log('\n##########################################')

		try:
			self.__validate_store__()
			self.__init_browser__()
		except Exception as err:
			self.logger.log('BROWSER CANT LAUNCH, err {}\n'.format(err))
			self.close_connection()
			sys.exit(0)

		self.logger.log('Attempting to login...')
		try:
			self.__login_insta_account__()
		except Exception as err:
			self.logger.log('LOGIN ERROR, CHECK CREDENTIALS, err: {}\n'.format(
				err))
			self.close_connection()
			sys.exit(0)
		else:
			self.logger.log('Login succeeded')

	def __validate_store__(self):
		self.store_list = settings.STORE_LIST.copy()

		for store in settings.STORE_LIST:
			if store not in self.supported_store_list:
				self.logger.log('Store {} not supported yet, will skip for \
				this store'.format(store))
				self.store_list.remove(store)
				
		if not self.store_list:
			raise Exception("No valid stores to check slots for..")

	@timeout.custom_decorator
	def __init_browser__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('log-level=3')
		options.add_argument('--window-size=1920x1080')
		options.add_argument('--no-sandbox')
		options.add_argument('--single-process')

		capabilities = DesiredCapabilities.CHROME.copy()
		capabilities['acceptSslCerts'] = True
		capabilities['acceptInsecureCerts'] = True

		self.browser = \
			webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH,
							 chrome_options=options,
							 desired_capabilities=capabilities)
		self.browser.delete_all_cookies()
		self.browser.get(self.url)
		time.sleep(3)

	@timeout.custom_decorator
	def __login_insta_account__(self):
		self.browser.find_element_by_link_text('Log in').click()
		time.sleep(1)
		xpath = '//*[@id="nextgen-authenticate.all.log_in_email"]'
		self.browser.find_element_by_xpath(xpath).send_keys(
			settings.INSTA_LOGIN_EMAIL)

		xpath = '//*[@id="nextgen-authenticate.all.log_in_password"]'
		self.browser.find_element_by_xpath(xpath).send_keys(
			settings.INSTA_LOGIN_PASS)
		time.sleep(0.5)

		login_title = self.browser.title
		xpath = '//*[@id="main-content"]/div[2]/form/div[3]/button'
		self.browser.find_element_by_xpath(xpath).click()
		time.sleep(3)
		if login_title == self.browser.title:
			raise Exception("Check instacart username/password")

	@timeout.custom_decorator
	def __check_delivery_slot__(self):
		xpath = \
			'//*[@id="header"]/div/div/div[4]/div[2]/div[2]/span/a/span'
		try:
			status = self.browser.find_element_by_xpath(xpath).text
		except timeout_decorator.TimeoutError:
			self.logger.log("TIMEOUT ERROR WITH CHECK_DELIVERY_SLOT")
			self.close_connection()
			raise RuntimeError("Restart program")
		except Exception as err:
			self.logger.log('RUNTIME ERROR WITH CHECK_DELIVERY_SLOT, \
			Err: {}'.format(err))
			self.close_connection()
			raise RuntimeError("Restart program")

		return ('NO_SLOT' if self.no_slot_msg in status else status)

	@timeout.custom_decorator
	def __get_address_book__(self, default_index):
		try:
			self.browser.find_elements_by_tag_name('button')[default_index].click()
			time.sleep(0.5)

			address_book = [(i, x.text) for (i, x) in
							enumerate(self.browser.find_elements_by_tag_name('button')) 
							if x.text and ',' in x.text]

			return address_book
		except timeout_decorator.TimeoutError:
			self.logger.log('TIMEOUT ERROR WITH GET_ADDRESS_BOOK \
			Index {}'.format(default_index))
			self.close_connection()
			raise RuntimeError("Restart program")
		except Exception as err:
			self.logger.log('RUNTIME ERROR WITH GET_ADDRESS_BOOK Index {}, \
			Err: {}'.format(default_index, err))
			self.close_connection()
			raise RuntimeError("Restart program")

	def log_msg(self, msg):
		self.logger.log(msg)

	@timeout.custom_decorator
	def __send_email__(self, slot_found_flag):
		msg = MIMEText(self.slots_result)
		if slot_found_flag:
			msg['Subject'] = 'Instacart slot information : SLOT_FOUND'
		else:
			msg['Subject'] = \
				'Instacart slot information : SLOT_NOT_FOUND'

		msg['From'] = settings.SENDER_GMAIL_ID
		msg['To'] = settings.RECEIVER_EMAIL_ID

		try:
			self.server.login(settings.SENDER_GMAIL_ID,
							  settings.SENDER_GMAIL_PASS)
			self.server.sendmail(settings.SENDER_GMAIL_ID,
								 settings.RECEIVER_EMAIL_ID,
								 msg.as_string())
			self.logger.log("Email notification succesfully sent")
		except Exception as err:
			self.logger.log('Exception with sending email, err : {}'.format(
				err))
			self.logger.log('Continuing finding slots.. check status from \
			console logs...')

	@timeout.custom_decorator
	def __get_default_slot__(self):
		try:
			def_addr_lst = [(i, x.text) for (i, x) in
							enumerate(self.browser.find_elements_by_tag_name('button')) 
							if x.text and len(x.text.split(' ')) > 2]
			if len(def_addr_lst) > 1:
				self.logger.log("Runtime error, found num_address : {}, \
				expected: 1".format(def_addr_lst))
				self.close_connection()
			else:
				def_addr_index = def_addr_lst[0][0]
				def_addr = \
					self.browser.find_elements_by_tag_name(
						'button')[def_addr_index].text
				return (def_addr_index, def_addr)
		except Exception as err:
			self.logger.log('NO ADDRESS FOUND IN INSTACART ACCOUNT')
			self.close_connection()
			sys.exit(0)

	@timeout.custom_decorator
	def __find_slot_curr_addr__(self, def_index, curr_index):
		try:
			self.browser.find_elements_by_tag_name(
				'button')[curr_index].click()
			time.sleep(6)
			tmp_addr = self.browser.find_elements_by_tag_name(
				'button')[def_index].text
			self.delivery_slot.append(
				(tmp_addr, self.__check_delivery_slot__()))

			self.browser.find_elements_by_tag_name('button')[def_index].click()
			time.sleep(0.5)
		except timeout_decorator.TimeoutError:
			self.logger.log('TIMEOUT ERROR WITH FINDING SLOT CURR ADDR {}, \
			DEF ADDR {}'.format(curr_index, def_index))
			self.close_connection()
			raise RuntimeError("Restart program")
		except Exception as err:
			self.logger.log('RUNTIME ERROR WITH FIND SLOT CURR ADDR {}, \
			DEF ADDR {}, Err: {}'.format(curr_index, def_index, err))
			self.close_connection()
			raise RuntimeError("Restart program")

	@timeout.custom_decorator
	def find_slots(self):
		self.slots_dict = {}
		num_address = 0
		default_address_id = None
		
		try:
			for store in self.store_list:
				self.slots_dict[store] = ''
				self.delivery_slot = []

				url = self.store_url.replace('costco', store)

				self.logger.log('Going to find slots for - {}...'.format(store))
				self.browser.get(url)
				time.sleep(10)

				(default_address_id, default_address) = \
					self.__get_default_slot__()

				self.delivery_slot.append(
					(default_address, self.__check_delivery_slot__()))

				num_address = self.__get_address_book__(default_address_id)

				if len(num_address) > 1:
					for (button_id, address) in num_address:
						if default_address[:10] != address[:10]:
							
							self.__find_slot_curr_addr__(
								default_address_id, button_id)

				self.slots_dict[store] = self.delivery_slot.copy()
		except Exception:
			self.close_connection()
			raise RuntimeError("Restart program")

	@timeout.custom_decorator
	def log_results(self):
		self.logger.log()
		self.slots_result = ''
		slot_found_once = False
		
		try:
			for (store, slot) in self.slots_dict.items():
				self.logger.log('{} slots :'.format(store))
				self.slots_result += '{} slots :\n'.format(store)

				slot.sort()

				for (addr, info) in slot:
					self.logger.log('\t{} : {}'.format(addr, info))
					self.slots_result += '\t{} : {}\n'.format(addr, info)

					if not slot_found_once and info != 'NO_SLOT':
						slot_found_once = True
				self.logger.log()
				self.slots_result += '\n'
		except Exception:
			self.close_connection()
			raise RuntimeError("Restart program")

		return slot_found_once

	def send_email(self, slot_found_status):
		if settings.SEND_GMAIL:
			self.__send_email__(slot_found_status)

	def refresh_browser(self):
		if self.browser:
			self.browser.refresh()
			time.sleep(1)
			
	def close_connection(self):
		if self.browser:
			self.browser.quit()
			self.logger.log('Connection ended')
		
		if self.server:
			try:
				self.server.quit()
			except Exception:
				pass

		self.logger.log('\n##########################################')
		


if __name__ == '__main__':

	def handler(signal_received, frame):

		msg = 'SIGINT or CTRL-C detected in main. Exiting gracefully'
		slot_finder.log_msg(msg)
		slot_finder.close_connection()
		sys.exit(0)

	signal(SIGINT, handler)

	slot_finder = InstaSlotFinder()
	slot_finder.start_browser()

	INTERVAL_BETWEEN_LOOPS = 60  # sec

	while True:

		slot_finder.log_msg('Starting new loop')
		try:
			slot_finder.find_slots()
			is_slot_found = slot_finder.log_results()
		except RuntimeError:
			slot_finder.log_msg('\nCreating new instance..\n')
			slot_finder = InstaSlotFinder()
			slot_finder.start_browser()
			continue
			
		if is_slot_found:
			slot_finder.log_msg('Slot found...')
			slot_finder.send_email(is_slot_found)
			break

		slot_finder.refresh_browser()
		time.sleep(INTERVAL_BETWEEN_LOOPS)

	slot_finder.close_connection()
	slot_finder.log_msg('Program ended\n')
