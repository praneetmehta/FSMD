from __future__ import unicode_literals
from __future__ import division
import urllib2
from bs4 import BeautifulSoup as bs
import youtube_dl as ydl
import json
import math
import eyed3
from GIS import AlbumArt as gimg
from ID3update import Song
import sys
import string
reload(sys)
sys.setdefaultencoding('utf-8')
songs = []

#searching youtube for song
def search(keyword):
	search = urllib2.quote(keyword)
	url = "https://www.youtube.com/results?search_query="+search
	response = urllib2.urlopen(url)
	html = response.read()
	soup = bs(html, 'html.parser');
	return soup


#get all links on page1 of youtube search
def grabLinks(parsed):
	for vid in parsed.findAll(attrs={'class':'yt-uix-tile-link'}):
		songs.append({'title':vid['title'], 'link':vid['href']})


#show search results
def showSearchResults():
	for i in range(0, len(songs)):
		try:
			print i+1,'- ',songs[i]['title']
		except:
			pass
	index = input('which song to download? enter index \t')-1
	return index
	

#youtube-dl logger
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)



#youtube-dl progress-hook
def my_hook(d):
    if d['status'] == 'finished':
    	global filename
        filename = d['filename'][:-4]+'mp3'
        print 'download complete, now downloading album art'
    else:
    	print (d['downloaded_bytes']*100)//d['total_bytes'],'%','\t','eta:',d['eta'],'sec'
    


#youtube-dl options object
ydl_opts = {	
				'format': 'bestaudio/best',
				    'postprocessors': [{
				        'key': 'FFmpegExtractAudio',
				        'preferredcodec': 'mp3',
				        'preferredquality': '192',
				    }],
				'logger': MyLogger(),
				'progress_hooks': [my_hook],
				'prefer_insecure':True
			}


#youtube-dl download
def downloadSong(i):
	songObj = songs[i]
	songLink = songObj['link']
	songTitle = songObj['title']
	with ydl.YoutubeDL(ydl_opts) as tube:
	    tube.download(['http://www.youtube.com'+songLink])

#download album art
def downloadAart(keyword):
	newImg = gimg(keyword)
	aapath = newImg.download()
	return aapath

def update(title,artist, keyword, filename, aapath, imgFormat):
	newSong = Song(title,artist, filename, keyword, aapath, imgFormat)
	newSong.updateID3();

if __name__ == '__main__':
	#user input for song to download
	filename = ' '
	title = raw_input('Enter song title: ')
	artist = raw_input('Enter artist name: ')
	album = raw_input('Enter album name: ')
	keyword = title + ' ' + album + ' ' + artist

	#function calls
	parsed = search(keyword)
	grabLinks(parsed)
	index = showSearchResults()
	downloadSong(index)
	aapath = downloadAart(keyword)
	imgFormat = aapath.split('.')[-1]
	update(string.capwords(title),string.capwords(artist), keyword, filename, aapath, imgFormat)

