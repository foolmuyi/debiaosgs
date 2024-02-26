# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,json,smtplib
from email.mime.text import MIMEText


class Monitor(object):
	def __init__(self):
		self.url = 'https://marknad.sgs.se/pgSearchResult.aspx#&seekAreaMode=simple&search=y&page=1&syndicateNo=1&objectMainGroupNo=1&companyNo=1&rent=0;15000&area=0;150&advertisement=-1&type=standard&take=1000000'
		self.file_dir = './roomList.json'
		self.mail_host = 'smtp.163.com'
		self.mail_username = 'xxxx@163.com'
		self.mail_pw = 'xxxx'
		self.mail_recv = ['xxxx@xxxx.xxx']

	def checkNewRoom(self):
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('headless')
		driver = webdriver.Chrome(options=chrome_options)
		driver.get(self.url)
		time.sleep(3)
		table = driver.find_element_by_css_selector('#search-container > table > tbody')
		results = table.find_elements_by_tag_name('tr')
		rooms_dict = {}
		with open(self.file_dir,'r') as f:
			old_rooms = json.load(f)
		old_rooms_name = list(old_rooms.keys())
		for each in results:
			infos = each.find_elements_by_tag_name('td')
			from_date = infos[0].text
			address = infos[2].text
			size = infos[5].text
			rent = infos[6].text.replace(' ','')
			name = address.splitlines()[0]
			plan = address.splitlines()[1]
			if (name not in old_rooms_name) and (int(from_date[-5:-3])>=8) and (int(rent)<=5500):
				mail_content = 'Room Info:'+'\n\n'+'From: '+from_date+'\n'+'Address: '+address.replace('\n',' ')+'\n'+'Plan: '+plan+'\n'+'Size: '+size+'\n'+'Rent: '+rent
				self.sendMail(mail_content)
			rooms_dict[name] = {'From':from_date, 'Address':address, 'Plan':plan, 'Size':size, 'Rent':rent}
		with open(self.file_dir,'w') as f:
			json.dump(rooms_dict,f,ensure_ascii=False,indent=1)
		driver.quit()

	def sendMail(self,mail_content):
		message = MIMEText(mail_content,'plain','utf-8')
		message['Subject'] = 'New room found'
		message['From'] = self.mail_username
		message['To'] = self.mail_recv[0]
		smtpObj = smtplib.SMTP()
		smtpObj.connect(self.mail_host,25)
		smtpObj.login(self.mail_username,self.mail_pw)
		smtpObj.sendmail(self.mail_username,self.mail_recv[0],message.as_string())
		smtpObj.quit()

def main():
	monitor = Monitor()
	monitor.checkNewRoom()


if __name__ == '__main__':
	main()