# Instacart-delivery-slot-finder
A Windows / Linux based python module to find Instacart slots and email you the status

# Inspirations:
Personally I was stuck with COVID-19 pandaemic at home for getting my day to day essentials and started looking online grocery delivery services like Instacart and other similar platforms. 

One challange with those platforms is finding slots in my area due to surge in demand for those services and it's nearly impossible for me to get a slot.

When checking with my friends and colleagues, I found most of us have the same problem and it's worse for elderly people as I got to know that they have to visit local stores for their daily essentials.
	
This tool was created to help people who are at high risk and those needy ones (including myself)
	
# Installation:

1. Windows:

        a. Python : v3 and above and python pip3
        b. Latest google chrome and chromedriver corresponding to chrome version installed
	  
2. Ubuntu:
	
          sudo ./install_ubuntu.sh # under 'install/' directory
          **Note : This tool will auto upgrade chrome to latest version, if not installed on the host pc already
	
  
3. Installing python modules:

          pip3 install -r requirements.txt
		  

# Limitations:

1. Supports email based login with credentials (ie) It doesn't support google / facebook based login

2. Preconfigure your home / delivery address in your instacart account once (ie) It doesn't support custom address check through this script

3. Checks for "Delivery" slots only (ie) Pickup slots are not supported

4. Supports GMAIL based notifications only


# How to use the tool 

1. Configure the settings.py file

	a. STORE_LIST = ['costco', 'safeway'] => Your desired stores, you can add as many as you want to check from the supported stores list.

		Current supported stores are (Just randomly tested! ):
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

	b. Provide your instacart login details. 
  
		INSTA_LOGIN_EMAIL = "<your_instacart_email_id>"
		INSTA_LOGIN_PASS = "<your_instacart_password>"
		
		Note: Only email based logins work, facebook / google based logins will not work
		
	c. Receiving email notification:
  
		If you wish to receive email notification, you need to configure below fields
		
		If you want to skip email configuration, you will still get the logs printed on console and in log file under 'logs/' directory
		
		SEND_GMAIL = True
		SENDER_GMAIL_ID = "<YOUR_GMAIL_ID>"
		SENDER_GMAIL_PASS = "<YOUR_GMAIL_PASSWORD/App specific password>"
		RECEIVER_EMAIL_ID = "<EMAIL_ID_TO_RECIVE_NOTIFICATIONS>"
		
		If you have enabled Two factor authenticatoin, you can proivide App specific password generated, follow : https://support.google.com/accounts/answer/185833?hl=en
		If you don't enabled 2FA, then you need to provide gmail password and need to 
		turn on "allow less secure apps from your gmail id" 
		#Steps:
		#1. GOTO : https://myaccount.google.com/u/0/lesssecureapps?pageId=none
		#2. Turn on : "Allow less secure apps"



2. Executing the script:
		
		Note : Make sure you have updated settings.py
		
		> python3 ./instacart_slot_finder.py
		

3. Stopping the script:

	By default, the script will run on loop indefinitely, if you want to stop execution, you can press 'ctrl + c'
		

4. Logs:
	
	Logs will be generated under logs/ folder
	
	Also, logs will be printed on console
	
		
# Sample Output: 

	##########################################
	(19:58:45) root | Going to init browser
	(19:58:45) root | Input Config:
	(19:58:45) root | 	Chrome driver path: C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe
	(19:58:45) root | 	Stores List: ['costco']
	(19:58:45) root | 	Instacart Login: xxxx@gmail.com
	(19:58:45) root | 	SEND_GMAIL report: True
	(19:58:45) root | 
	##########################################
	(19:58:56) root | Attempting to login...
	(19:59:04) root | Login succeeded
	(19:59:04) root | Starting new loop
	(19:59:04) root | Going to find slots for - costco...
	(19:59:56) root | 
	(19:59:56) root | costco slots :
	(19:59:56) root | 	<YOUR_ADDRESS_1> : Arrives Tomorrow - Apr 16

	(19:59:56) root | Sending email notification
	(20:00:22) root | SIGINT or CTRL-C detected. Exiting gracefully
	(20:00:25) root | Connection ended
	(20:00:25) root | 
	##########################################

# Tested platforms:
Tested on Windows 10 and Ubuntu 16.04

Note: As I don't have personal macbook, I can't able to test. If you have one, please try on Mac and let me know if it works.

# Tested tool versions:
	Python3
	Google Chrome 81.0.4044.92
	Chromedriver v81.0.4044.92
	selenium v3.141.0		
	
# Known Issues:

1. If the previous session was terminated abrubptly / incorrectly, subsequent script exeuction may cause incorrect results
	
	- I have handled this issue (using signal handlers), but still I get this issue in rare times (may be 1 in 50 exeuctions)
	
# Disclaimer:

	No guarantee that you will get the slots as reported by tool, as the slot booking happens at realtime.

	This tools is for personnal-noncommercial use only.
