# FSMD - Fucking Sexy Music Downloader

- Add a folder named downloadedSongs in the root directory of scripts. Or if you wish to add any other folder, change         downloadDirectory varialble in FSMD.py

- For simply downloading a song, run

  `python FSMD.py`
  
- For batch downloads, modify the csv file 'batch.csv' (do not remove the headers) and add all the songs you wish to download and the amount of info you have. After updating the csv, run

  `python FSMD.py -b batch.csv`
  
   The script will automatically do its job. Sit back and relax

- Extra python modules and dependencies
  - mechanize
  - eyed3
  - pathlib
  - youtube_dl
  - requests
  
- Install pip

  `sudo apt-get install python-pip`
  
- Install the modules

  `sudo -H pip install <module name>`

# Future Plans
 - GUI
 - Multithreading support for tasks like music download and album art download
 - Blitzr API support for better and robust metadata fetching
 - A Way to automatically identify title
 - More download modes and alternative actions
