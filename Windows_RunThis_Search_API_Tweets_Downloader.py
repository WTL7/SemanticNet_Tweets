import sys
import subprocess
import os               

# This setting is very important to avoid errors in windows
os.environ['PYTHONIOENCODING'] = 'utf-8'    #setting the sys environment, or we will get unicoden error   
file1 = "Search_API_Tweets_Downloader.py"   # put the file you want to run simultanously 
proc = subprocess.Popen([sys.executable,file1])

      