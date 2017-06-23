from __future__ import unicode_literals
from __future__ import division
import urllib2
from bs4 import BeautifulSoup as bs #module for parsing html
import youtube_dl as ydl #youtube_dl for downloading youtube videos and mp3
from GIS import AlbumArt as gimg #custom module for fetching album arts
from ID3update import Song #custom module for fetchid metadata and updating the downloaded file
import string
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')



#searching youtube for song
def search(keyword):
	print 'search keyword --- ', keyword
	search = urllib2.quote(('').join(keyword.split('@')))
	url = "https://www.youtube.com/results?search_query="+search
	response = urllib2.urlopen(url)
	html = response.read()
	soup = bs(html, 'html.parser');
	return soup


#get all links on page1 of youtube search
def grabLinks(parsed):
	del songs[:]
	for vid in parsed.findAll(attrs={'class':'yt-uix-tile-link'}):
		if vid.find_next_sibling('span').get_text() == ' - Playlist':
			pass
		else:
			songs.append({'title':vid['title'], 'link':vid['href']})



#show search results
def showSearchResults():
	if execType == '-b':
		print 'downloading --- '+songs[0]['title']
		index = 0
		return index
	elif execType == '-d':
		for i in range(0, len(songs)):
			try:
				print i+1,'- ',songs[i]['title']
			except:
				pass
		return input('which song to download? enter index \t')-1
	

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
	global filename
	if d['status'] == 'finished':
		print "d['filename']",d['filename']
		print filename[-4:]
		if d['filename'][-4:] == 'webm':
		# global filename
			filename = d['filename'][:-4]+'mp3'
		elif d['filename'][-4:] == '.m4a':
		# global filename
			filename = d['filename'][:-3]+'mp3'
		print filename
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

def update(keyword, filename, aapath, imgFormat, dd):
	newSong = Song(keyword, filename, aapath, imgFormat, dd)
	newSong.updateID3();

def execute(keyword, extra=''):
	try:
		parsed = search(keyword+extra)
		grabLinks(parsed)
		index = showSearchResults()
		downloadSong(index)
		aapath = downloadAart(keyword)
		imgFormat = aapath.split('.')[-1]
		update(string.capwords(keyword), filename, aapath, imgFormat, downloadDirectory)
	except KeyboardInterrupt:
		print '\nKeyboard Interrupt. Now exiting'
		print "\nGood Bye :')"
		sys.exit()
	except:
		print '\nSome unexpected error occured, Pleej try again :P'

if __name__ == '__main__':
	execType = '-d'
	songs = []
	batch = []
	filename = 'Unknown'
	downloadDirectory = 'downloadedSongs/'

	try:
		execType = sys.argv[1]
		batchCSV = sys.argv[2]
		if execType == '-b':
			if os.path.isfile(batchCSV):
				with open(batchCSV, 'rb') as csvfile:
					batchlist = csv.DictReader(csvfile)
					for row in batchlist:
						batch.append(row['Title'] + ' @' + row['Artist'] + ' @' + row['Album'])
				for batchitem in batch:
					print 'batchitem --- '+batchitem
					execute(batchitem, ' official audio')
			else:
				print 'csv '+ batchCSV +' does not exist'
			# print batchlist.types
		else:
			print 'invalid argument'
		
	except:
		if len(sys.argv)>1:
			print '\nusage:\n\t', 'python FSMD.py <arg1> <arg2>\n\n','>>> if batch downloading, arg1 = -b and arg2 = path of .csv\n', '>>> for single file download no argument required, simply run python FSMD.py'
		else:
			title = raw_input('Enter song title:\n>>> ')
			artist = raw_input('Enter artist name:\n>>> ')
			album = raw_input('Enter album name:\n>>> ')
			keyword = title + ' @' + artist + ' @' + album
			execute(keyword)
	
	#user input for song to download
	

	#function calls
	

