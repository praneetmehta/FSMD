import urllib2
import eyed3
import mechanize
import os
from bs4 import BeautifulSoup as bs
import unicodedata as ud
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Song:
	def __init__(self, title, artist, filename, keyword, albumart, aaformat):
		self.filename = filename.encode('utf-8')
		self.keyword = urllib2.quote(keyword)
		self.albumart = albumart
		self.aaformat = aaformat
		self.album = 'Unknown'
		self.artist = artist
		self.title = title
		self.feat = ' '
		self.genre = 'Unknown'
		self.fetchID3()

	def fetchID3(self):
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]
		searchURL = "https://www.google.co.in/search?site=imghp&source=hp&biw=1414&bih=709&q="+self.keyword+urllib2.quote(' song')
		print searchURL
		html = browser.open(searchURL)
		soup = bs(html, 'html.parser')
		
		souplist = soup.findAll(attrs={'class':'_o0d'})
		for i in range(1,len(souplist)):
			if souplist[i].get_text().split(':')[0].lower() == 'album' or souplist[i].get_text().split(':')[0].lower() == 'movie':
				self.album = souplist[i].get_text().split(':')[1]
				print 'album ',souplist[i].get_text().split(':')[1]
			elif souplist[i].get_text().split(':')[0].lower() == 'artist' or souplist[i].get_text().split(':')[0].lower() == 'artists':
				self.artist = souplist[i].get_text().split(':')[1]
				print 'artist ',souplist[i].get_text().split(':')[1]
			elif souplist[i].get_text().split(':')[0].lower() == 'genre' or souplist[i].get_text().split(':')[0].lower() == 'genres':
				self.genre = souplist[i].get_text().split(':')[1]
				print 'genre ',souplist[i].get_text().split(':')[1]
			elif souplist[i].get_text().split(':')[0].lower() == 'featured artist' or souplist[i].get_text().split(':')[0].lower() == 'featured artists':
				self.feat = souplist[i].get_text().split(':')[1]
				print 'artist ',souplist[i].get_text().split(':')[1]
			else:
				pass
		self.fetchalbum()
		# try:
		# 	self.artist = id3[0].get_text()
			
		# except:
		# 	print 'error updating artist name'

		# try:
		# 	self.album = id3[1].get_text()
			
		# except:
		# 	print 'error updating album name'
	def fetchalbum(self):
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]
		searchURL = "https://www.google.co.in/search?site=imghp&source=hp&biw=1414&bih=709&q="+self.keyword+urllib2.quote(' album name')
		html = browser.open(searchURL)
		soup = bs(html, 'html.parser')
		for i in soup.findAll(attrs={'class':'_B5d'}):
			print i.get_text()

	def updateID3(self):		
		audiofile = eyed3.load(self.filename)
		try:
			audiofile.tag.artist = unicode(self.artist, "utf-8")
		except:
			audiofile.tag.artist = self.artist
			
		try:
			audiofile.tag.album = unicode(self.album, "utf-8")
		except:
			audiofile.tag.album = self.album

		title = ''
		if self.feat == ' ':
			title = self.title
		else:
			title = self.title+' feat. '+self.feat
		try:
			audiofile.tag.title = unicode(title, "utf-8")
		except:
			audiofile.tag.title = title
		try:
			audiofile.tag.genres = unicode(self.genre, "utf-8")
		except:
			audiofile.tag.genres = self.genre

		audiofile.tag.images.set(3, open(self.albumart,'rb').read(), 'image/'+self.aaformat)
		audiofile.tag.save()
		os.rename(self.filename, 'downloadedSongs/'+self.title+'.mp3')
		print 'update complete'
		
		os.remove(self.albumart)
# newsong = Song('Rockabye','Rockabye.mp3', 'rockabye','rockabye   album art.jpeg','jpeg')
# newsong.updateID3()