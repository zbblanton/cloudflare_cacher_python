import os
import requests
import json
import datetime
import time
import threading

cachable = ['css', 'js', 'jpeg', 'gif', 'ico', 'png', 'pdf', 'jpg', 'JPG', 'ttf', 'woff2', 'woff', 'tiff', 'json', 'eot', 'map', 'svg']

domain = 'http://blantontechnology.com'
rootdir = '/var/www/html/blantontechnology/newsite/'
web_data = {}

def timestamp():
 return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

def log(msg):
 print(timestamp() + ": " + msg)
 return

def scan_files():
  global web_data
  files_changed = False
  i = 0
  log("Scanning files...")
  #Scan for additions
  for subdir, dirs, files in os.walk(rootdir):
     for file in files:
         if os.path.join(subdir, file) not in web_data:
          files_changed = True
          current_obj = {}
          #current_obj['path'] = os.path.join(subdir, file)
          current_obj['url'] = domain + '/' + os.path.relpath(os.path.join(subdir, file), rootdir)
          current_obj['date'] = str(os.path.getmtime(os.path.join(subdir, file)))
          #current_obj['cached_date'] = str(os.path.getmtime(os.path.join(subdir, file)))
          current_obj['cached_date'] = 0.0
          if os.path.splitext(file)[1][1:] in cachable:
              current_obj['cachable'] = "true"
              #response = requests.head(c['url'])
              #print(response.headers['CF-Cache-Status'])
          else:
              current_obj['cachable'] = "false"
          log("Adding: " + os.path.join(subdir, file))
          web_data[os.path.join(subdir, file)] = current_obj
          i = i + 1

  #Scan for removals or changes
  removal_list = []
  for key, value in web_data.iteritems():
   if not os.path.isfile(key):
    files_changed = True
    log("Removing: " + key)
    removal_list.append(key)
   else: #Check for file updates
    if os.path.getmtime(os.path.join(subdir, key)) > float(value['date']):
     files_changed = True
     value['date'] = os.path.getmtime(os.path.join(subdir, key))
     value['cached_date'] = 0.0
     log("Changed: " + key)
  for i in range(len(removal_list)):
   print(removal_list)
   web_data.pop(removal_list[i], None)

  log("Completed scan...")
  return files_changed

def cache_files():
 global web_data
 files_cached = False

 for i in web_data:
  if((float(web_data[i]['cached_date']) == 0.0 or float(web_data[i]['cached_date']) >= (time.time() + (30 * 86400))) and web_data[i]['cachable'] == "true"):
   files_cached = True
   response = requests.head(web_data[i]['url'])
   web_data[i]['cached_date'] = str(time.time())
   log('CF-Cache-Status = ' + response.headers['CF-Cache-Status'] + ' ' + web_data[i]['url'])

 if(files_cached == True):
   log("Writing cache changes to data.json...")
   with open('data.json', 'w') as outfile:
     json.dump(web_data, outfile)
   log("Writing complete.")

def init():
 global web_data
 #Check if data.json is a file, if it is, load the data, if not create it and scan for files.
 if os.path.isfile("data.json"):
  log("Found data.json")
  log("Loading file into RAM...")
  with open('data.json') as json_data:
    web_data = json.load(json_data)
    #print(web_data["/var/www/html/blantontechnology/newsite/inc/bootstrap/fonts/glyphicons-halflings-regular.svg"]) #testing that the file loaded correctly
  if(scan_files() == True):
   log("Writing changes to data.json...")
   with open('data.json', 'w') as outfile:
     json.dump(web_data, outfile)
   log("Writing complete.")
 else:
  log("Could not find data.json")
  log("Writing data.json...")
  scan_files()
  with open('data.json', 'w') as outfile:
    json.dump(web_data, outfile)
  log("Writing complete.")


init()
cache_files()

#def main_loop():
# threading.Timer(60.0, hello_world).start() # called every minute
# print("Hello, World!")
