import urllib2
import urllib
from bs4 import BeautifulSoup as bs
import mechanize
import os
import imghdr
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')

class AlbumArt:
	def __init__(self, keyword):
		self.keyword = urllib2.quote(keyword+' album art')
		self.searchURL()

	def searchURL(self):
		header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
		searchURL = "https://www.google.co.in/search?q="+self.keyword+"&source=lnms&tbm=ischself.keyword"
		soup = bs(urllib2.urlopen(urllib2.Request(searchURL,headers=header)),'html.parser')
		# browser = mechanize.Browser()
		# browser.set_handle_robots(False)
		# browser.addheaders = [('User-agent','Mozilla')]
		# searchURL = "https://www.google.co.in/search?q="+self.keyword+"&source=lnms&tbm=ischself.keyword"
		# html = browser.open(searchURL)
		# soup = bs(html, 'html.parser')
		self.findImg(soup)

	def findImg(self, soup):
		for a in soup.findAll(attrs={"class":"rg_meta"}):
		    self.link =json.loads(a.text)["ou"]
		    break

	def download(self):
		downloader = urllib.URLopener()
		downloader.retrieve(self.link, urllib2.unquote(self.keyword))
		print 'album art download complete'
		imgFormat = imghdr.what(urllib2.unquote(self.keyword))
		os.rename(urllib2.unquote(self.keyword), urllib2.unquote(self.keyword)+'.'+imgFormat)
		print 'format attached as ',imgFormat
		name = urllib2.unquote(self.keyword)+'.'+imgFormat
		return name
		
