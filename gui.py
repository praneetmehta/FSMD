from Tkinter import *
import tkFont
import ttk, tkFileDialog

class GUI(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.font = tkFont.Font(family="Times")
		self.style = ttk.Style().configure('.', font=self.font)
		self.file_ = None
		self.initialize()
	
	def initialize(self):
		# initializes the two tabs
		self.tabs = ttk.Notebook(self, padding=5,width=550)
		self.tab1 = ttk.Frame(self.tabs)
		self.tab2 = ttk.Frame(self.tabs)
		self.tabs.add(self.tab1, text="Single Download")
		self.tabs.add(self.tab2, text="Batch Download")
		self.tabs.grid(row=0, rowspan=8, columnspan=4)
		
		# widgets inside tab1 (Single Download) - Grid Layout used
		self.songLabel = Label(self.tab1, text="Song Title", font=self.font).grid(row=0, column=0, columnspan=2, rowspan=2,
               sticky=W+E+N+S, padx=5, pady=5)
		self.artistLabel = Label(self.tab1, text="Artist", font=self.font).grid(row=2, column=0, columnspan=2, rowspan=2,
               sticky=W+E+N+S, padx=5, pady=5)
		self.albumLabel = Label(self.tab1, text="Album Name", font=self.font).grid(row=4, column=0, columnspan=2, rowspan=2,
               sticky=W+E+N+S, padx=5, pady=5)
		self.song = Entry(self.tab1, font=self.font, width = 50)
		self.song.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)
		self.artist = Entry(self.tab1, font=self.font)
		self.artist.grid(row=2, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)
		self.album = Entry(self.tab1, font=self.font)
		self.album.grid(row=4, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)
		self.download = Button(self.tab1, text="Download", font=self.font, command=self.func)
		self.download.grid(row=6,column=0, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=5, pady=5)
		
		# widgets inside tab2 (Batch Download) - file Browser added	
		self.browse = Button(self.tab2, text="Browse", font=self.font, command=self.browseFile)
		self.browse.grid(row=2, rowspan=2, column=0, padx=20, pady=10)
		self.fileLabel = Label(self.tab2, text="No File Selected", font=self.font)
		self.fileLabel.grid(row=2, rowspan=2, column=1, pady=10)
		self.downloadAll = Button(self.tab2, text="Download All", font=self.font)
		self.downloadAll.grid(row=6, rowspan=2, columnspan=2, pady=10)
		
		# Area to display console messages
		self.console = Text(self, bg='black',fg='white',height=10, width=70, font=self.font)
		self.console.grid(row=11, rowspan=2, columnspan=4, column=0, padx = 10, pady= 10)
		self.console.insert(INSERT, "Console Messages Here.")
		
		# Scroll bar for the console window
		self.scroll = Scrollbar(self, command=self.console.yview)
		self.scroll.grid(row=11, rowspan=2, pady=10, column=4, sticky='NSEW')
		self.console['yscrollcommand'] = self.scroll.set
		
		# Frame containing Input option for user to select the song to download
		self.bottomFrame = Frame(self, bd=5)
		self.bottomFrame.grid(row=13, column=0, columnspan=4)
		self.indexLabel = Label(self.bottomFrame, text="Song Index", font=self.font).grid(row=0, column=0, rowspan=3, columnspan=1, padx=5, pady=5)
		self.index = Entry(self.bottomFrame, font=self.font).grid(row=0, column=1, rowspan=3, columnspan=1, padx=5, pady=5)
		self.submit = Button(self.bottomFrame, text="Submit Choice", font=self.font).grid(row=0, column=2, rowspan=3, columnspan=1, padx=5, pady=5)
		
	def browseFile(self):
		try:
			self.file_ = tkFileDialog.askopenfile(parent=self.tab2, mode='rb', title='Choose a file')
			self.fileLabel['text'] = self.file_.name
		except:
			self.file_ = None     # Need to change this part so that previous file remains
			self.fileLabel['text'] = "No File Selected"
	
	def func(self):
		print "Song Title: ", self.song.get()
		print "Album: ", self.album.get()
		print "Artist: ", self.artist.get()
		# Call appropriate function here to search for songs.
		
# Yet to be integrated with the main application
# For checking the GUI, just use "python gui.py"
if __name__ == '__main__':
	app = GUI(None)
	app.title('Music Downloader')
	app.mainloop()
