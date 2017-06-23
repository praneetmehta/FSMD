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
	def __init__(self, keyword, filename, albumart, aaformat, dd='downloadedSongs/'):
		self.info = keyword.split('@')
		self.filename = filename.encode('utf-8')
		print 'self.filename ',self.filename
		self.keyword = urllib2.quote(('').join(self.info))
		self.albumart = albumart
		self.aaformat = aaformat
		self.album = 'Single'
		self.artist = self.info[1]
		self.title = self.info[0]
		self.feat = ' '
		self.genre = 'Unknown'
		self.dd = dd
		self.fetchID3()

	def fetchID3(self):
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]
		searchURL = "https://www.google.co.in/search?site=imghp&source=hp&biw=1414&bih=709&q="+urllib2.quote(self.title+' '+self.artist+' song')
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
				print 'featured artist ',souplist[i].get_text().split(':')[1]
			else:
				pass
		self.fetchalbum()
		
		
	def fetchalbum(self):
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]
		searchURL = "https://www.google.co.in/search?site=imghp&source=hp&biw=1414&bih=709&q="+urllib2.quote(self.title+' '+self.artist+' album name')
		html = browser.open(searchURL)
		soup = bs(html, 'html.parser')
		for i in soup.findAll(attrs={'class':'_B5d'}):
			if self.album == 'Single':
				self.album = i.get_text()
			break

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
			audiofile.tag.genre = unicode(self.genre, "utf-8")
		except:
			audiofile.tag.genre = self.genre

		audiofile.tag.images.set(3, open(self.albumart,'rb').read(), 'image/'+self.aaformat)
		audiofile.tag.save()
		if not os.path.isfile('downloadedSongs/'+title+'.mp3'):
			os.rename(self.filename, self.dd+title+'.mp3')
		else:
			newTitle = raw_input('Similar file already exits, enter new file name: ')
			os.rename(self.filename, self.dd+newTitle+'.mp3')
		print 'update complete'
		
		os.remove(self.albumart)
# newsong = Song('Rockabye','Rockabye.mp3', 'rockabye','rockabye   album art.jpeg','jpeg')
# newsong.updateID3()
