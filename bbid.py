#!/usr/bin/env python3
import os, sys, urllib.request, re, threading, posixpath, urllib.parse, argparse, atexit, random, socket, time, hashlib, pickle, signal

#config
output_dir = './bing' #default output dir
adult_filter = True #Do not disable adult filter by default
pool_sema = threading.BoundedSemaphore(value = 20) #max number of download threads
bingcount = 35 #default bing paging
socket.setdefaulttimeout(4)

in_progress = []
tried_urls = []
finished_keywords=[]
def download(url,output_dir):
	global tried_urls
	url_hash=hashlib.sha224(url.encode('utf-8')).digest()
	if url_hash in tried_urls:
		return
	pool_sema.acquire() 
	path = urllib.parse.urlsplit(url).path
	filename = posixpath.basename(path)
	if len(filename)>40:
		filename=filename[:36]+filename[-4:]
	while os.path.exists(r'bing/'+output_dir + '/' + filename):
		filename = str(random.randint(0,100)) + filename
	in_progress.append(filename)
	try:
		urllib.request.urlretrieve(url, r'bing/'+output_dir + '/' + filename)
		in_progress.remove(filename)
		print("OK " + filename)
	except:
		print("FAIL " + filename)
	tried_urls.append(url_hash)
	pool_sema.release()

def removeNotFinished():
	for filename in in_progress:
		try:
			os.remove(output_dir + '/' + filename)
		except FileNotFoundError:
			pass

def fetchImagesFromKeyword(keyword,output_dir):
	current = 1
	last = ''
	while True:
		response = urllib.request.urlopen('https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keyword) + '&async=content&first=' + str(current) + '&adlt=' + adlt)
		html = response.read().decode('utf8')
		links = re.findall('imgurl:&quot;(.*?)&quot;',html)
		try:
			if links[-1] == last:
				break
			last = links[-1]
			current += bingcount
			for link in links:
				t = threading.Thread(target = download,args = (link,output_dir))
				t.start()
		except IndexError:
			print('No search results for "{0}"'.format(keyword))
			return False
		time.sleep(0.1)
	return True

def backup_history(*args):
	download_history=open('download_history.pickle','wb')
	pickle.dump(tried_urls,download_history)
	pickle.dump(finished_keywords, download_history)
	download_history.close()
	print('history_dumped')
	if args:
		exit(0)
	
if __name__ == "__main__":
	atexit.register(removeNotFinished)
	parser = argparse.ArgumentParser(description = 'Bing image bulk downloader')
	parser.add_argument('-s', '--search-string', help = 'Keyword to search', required = False)
	parser.add_argument('-f', '--search-file', help = 'Path to a file containing search strings line by line', required = False)
	parser.add_argument('-o', '--output', help = 'Output directory', required = False)
	parser.add_argument('--filter', help = 'Enable adult filter', action = 'store_true', required = False)
	parser.add_argument('--no-filter', help=  'Disable adult filter', action = 'store_true', required = False)
	args = parser.parse_args()
	if (not args.search_string) and (not args.search_file):
		parser.error('Provide Either search string or path to file containing search strings')	 
	
	signal.signal(signal.SIGINT, backup_history)
	signal.signal(signal.SIGTSTP, backup_history)
	try:
		download_history=open('download_history.pickle','rb')
		tried_urls=pickle.load(download_history)
		finished_keywords=pickle.load(download_history)
		download_history.close()
	except (OSError, IOError):
		tried_urls=[]
	if adult_filter:
		adlt = ''
	else:
		adlt = 'off'
	if args.no_filter:
		adlt = 'off'
	elif args.filter:
		adlt = ''
	if args.search_file:
		try:
			inputFile=open(args.search_file)
		except (OSError, IOError):
			print("Couldn't open file {}".format(args.search_file))
			exit(1)
		
		for keyword in inputFile.readlines():
			keyword_hash=hashlib.sha224(keyword.strip().encode('utf-8')).digest()
			if keyword_hash in finished_keywords:
				print('Skipping {0}'.format(keyword.strip()))
				continue
			output_dir=keyword.strip().replace(' ','_')
			if not os.path.exists(r'bing/'+output_dir):
				os.makedirs(r'bing/'+output_dir)
			if fetchImagesFromKeyword(keyword,output_dir):
				finished_keywords.append(keyword_hash)
			backup_history()
		inputFile.close()
	elif args.search_string:	
		if args.output:
			output_dir = args.output
	
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		keyword = args.search_string
		fetchImagesFromKeyword(keyword,output_dir)
	backup_history()

	
