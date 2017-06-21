import urllib2
import urllib
from bs4 import BeautifulSoup as bs
import mechanize
import os
import imghdr
import sys
import requests
import json
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
		searchURL = "https://www.google.co.in/search?q="+self.keyword+"&source=lnms&tbm=isch"
		soup = bs(urllib2.urlopen(urllib2.Request(searchURL,headers=header)),'html.parser')
		print searchURL
		self.findImg(soup)


	def findImg(self, soup):
		'''attempts to find the image link one by one for five
		 attempts or else if an error occurs switch to default image'''
		imageindex = self.attemptcount
		try:
			print 'trying '+str(self.attemptcount)+' image'
			if imageindex == 0:
				self.linklist = soup.findAll(attrs={"class":"rg_meta"})
			else:
				pass
			a = self.linklist[imageindex]
			self.link =json.loads(a.text)["ou"]
			print self.link
		except:
			self.link = self.defaultlink
		# if attemptcount = 0 download is called from the main script or else it has to invoked from here
		if(self.attemptcount == 0):
			pass
		else:
			self.download()


	def download(self):
		'''downloads the image'''
		r = requests.get(self.link)
		if r.status_code == 200:
			pass
		else:
			print 'image download error, downloading default album art'
			self.link = self.defaultlink
			r = requests.get(self.link)
		with open(urllib2.unquote(self.keyword), 'w+') as outfile:
		    outfile.write(r.content)
		print 'album art download complete'
		self.imgFormat = imghdr.what(urllib2.unquote(self.keyword))
		print self.imgFormat
		if self.imgFormat is not None:
			self.attachFormat()
		else:
			self.attemptcount += 1
			if self.attemptcount < 5:
				self.findImg(' ')
			else:
				self.link = self.defaultlink
				self.download()
		
	def attachFormat(self):
		os.rename(urllib2.unquote(self.keyword), urllib2.unquote(self.keyword)+'.'+self.imgFormat)
		print 'format attached as ',self.imgFormat
		name = urllib2.unquote(self.keyword)+'.'+self.imgFormat
		return name
		
		
# newimg = AlbumArt('pehli dafa @ @atif aslma')
# newimg.download()