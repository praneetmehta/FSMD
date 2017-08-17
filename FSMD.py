from __future__ import unicode_literals
from __future__ import division
import urllib2
from bs4 import BeautifulSoup as bs #module for parsing html
import youtube_dl as ydl #youtube_dl for downloading youtube videos and mp3
from GIS import AlbumArt as gimg #custom module for fetching album arts
from ID3update import Song #custom module for fetchid metadata and updating the downloaded file
from gui import *
import string
import csv
import time
import os
import sys
import progressBar

pb = progressBar.progressor('linear')

reload(sys)
sys.setdefaultencoding('utf8')



#searching youtube for song
def search(keyword):
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
		if vid.find_next_sibling('span').get_text() == ' - Playlist' or vid.find_next_sibling('span').get_text() == ' - Channel':
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
		for i in range(0, 10):
			try:
				print i+1,'- ',songs[i]['title']
			except:
				pass
		return input('which song to download? enter index \t')-1
	

#youtube-dl logger
class dl_logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)



#youtube-dl progress-hook
def prog_hook(d):
	global filename
	global pb
	if d['status'] == 'finished':
		pb.stop()
		if d['filename'][-4:] == 'webm':
		# global filename
			filename = d['filename'][:-4]+'mp3'
		elif d['filename'][-4:] == '.m4a':
		# global filename
			filename = d['filename'][:-3]+'mp3'
		print('\n')
		print 'download complete'
	else:
		percent = (d['downloaded_bytes']*100)//d['total_bytes']
		pb.update(percent, d['eta'])
		sys.stdout.flush()
    


#youtube-dl download
def downloadSong(i):
	global pb
	songObj = songs[i]
	songLink = songObj['link']
	songTitle = songObj['title']
	with ydl.YoutubeDL(ydl_opts) as tube:
		pb.start()
		tube.download(['http://www.youtube.com'+songLink])
	

#download album art
def downloadAart(keyword, downloadDirectory):
	newImg = gimg(keyword, downloadDirectory)
	aapath = newImg.download()
	return aapath

def update(keyword, filename, aapath, imgFormat, dd):
	newSong = Song(keyword, filename, aapath, imgFormat, dd)
	newSong.updateID3();

def execute(keyword, downloadDirectory, extra=''):
	global pb
	try:
		parsed = search(keyword+extra)
		grabLinks(parsed)
		index = showSearchResults()
		print('\n')
		if execType == '-d':
			try:
				clear = lambda: os.system('clear')
				clear()
			except:
				pass
		else:
			pass
		downloadSong(index)
		aapath = downloadAart(keyword, downloadDirectory)
		imgFormat = aapath.split('.')[-1]
		update(string.capwords(keyword), filename, aapath, imgFormat, downloadDirectory)
		return True
	except KeyboardInterrupt:
		print 'Keyboard Interrupt. Now exiting'
		print "Good Bye :')"
		pb.stop()
		sys.exit()
	except:
		print '\nSome unexpected error occured, Please try again :P'
		try:
			pb.stop()
		except:
			pass
		return False

if __name__ == '__main__':
	print('FSMD v2')
	print('Author: Paneer\n')
	time.sleep(1.5)
	execType = '-d'
	songs = []
	batch = []
	filename = 'Unknown'
	downloadDirectory = '/home/praneet/Music/'

	#youtube-dl options object
	ydl_opts = {	
					'format': 'bestaudio/best',
					    'postprocessors': [{
					        'key': 'FFmpegExtractAudio',
					        'preferredcodec': 'mp3',
					        'preferredquality': '192',
					    }],
					'outtmpl': downloadDirectory+'%(title)s.%(ext)s',
					'logger': dl_logger(),
					'progress_hooks': [prog_hook],
					'prefer_insecure':True
				}

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
					execute(batchitem, downloadDirectory, ' official audio')
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
			execute(keyword, downloadDirectory)
	
	#user input for song to download
	

	#function calls
	

