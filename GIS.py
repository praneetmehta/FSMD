import urllib2
from bs4 import BeautifulSoup as bs
import os
import imghdr
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class AlbumArt:
	def __init__(self, keyword):
		'''initializer'''
		self.info = keyword.split('@')
		self.keyword = urllib2.quote(('').join(self.info)+' album art')
		self.defaultlink = "http://www.kirkville.com/wordpress/wp-content/uploads/itunes-no-artwork.png"
		self.attemptcount = 0
		self.searchURL()

	def searchURL(self):
		'''fetches the google search images page 
		with the given search keyword and parses it'''
		header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		searchURL = "https://www.google.co.in/search?q="+self.keyword+"&source=lnms&tbm=isch&tbs=iar:s"
		soup = bs(urllib2.urlopen(urllib2.Request(searchURL,headers=header)),'html.parser')
		self.findImg(soup)


	def findImg(self, soup):
		'''attempts to find the image link one by one for five
		 attempts or else if an error occurs switch to default image'''
		self.linklist = soup.findAll(attrs={"class":"rg_meta"})
		# a = self.linklist[imageindex]
		# self.link =json.loads(a.text)["ou"]
		# except:
		# 	self.link = self.defaultlink
		# # if attemptcount = 0 download is called from the main script or else it has to invoked from here
		# if(self.attemptcount == 0):
		# 	pass
		# else:
		# 	self.download()


	def download(self):
		'''downloads the image'''
		for i in enumerate(self.linklist):
			self.link =json.loads(i[1].text)["ou"]
			r = requests.get(self.link)
			print('trying image #{}'.format(i[0]))
			if(r.status_code == 200):
				break
			elif i[0] > 4:
				self.link = self.defaultlink
				break
			else:
				pass

		with open(urllib2.unquote(self.keyword), 'w+') as outfile:
			outfile.write(r.content)
		print 'album art download complete'
		self.imgFormat = imghdr.what(urllib2.unquote(self.keyword))
		if self.imgFormat is not None:
			aaformat = self.attachFormat()
			return aaformat
		else:
			print('Network Error')
			sys.exit()
			

		
	def attachFormat(self):
		os.rename(urllib2.unquote(self.keyword), urllib2.unquote(self.keyword)+'.'+self.imgFormat)
		print 'format attached as ',self.imgFormat
		return urllib2.unquote(self.keyword)+'.'+self.imgFormat
		
		
		
# newimg = AlbumArt('pehli dafa @ @atif aslma')
# newimg.download()
