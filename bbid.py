#!/usr/bin/env python3
import os, sys, urllib.request, re, threading, posixpath, urllib.parse, argparse, atexit, random

#config
output_dir = './bing' #default output dir
adult_filter = True #Do not disable adult filter by default
pool_sema = threading.BoundedSemaphore(value = 20) #max number of download threads
bingcount = 35 #default bing paging

in_progress = []
def download(url):
	pool_sema.acquire() 
	path = urllib.parse.urlsplit(url).path
	filename = posixpath.basename(path)
	while os.path.exists(output_dir + '/' + filename):
		filename = str(random.randint(0,100)) + filename
	in_progress.append(filename)
	try:
		urllib.request.urlretrieve(url, output_dir + '/' + filename)
		in_progress.remove(filename)
		print("OK " + filename)
	except:
		print("FAIL " + filename)
	pool_sema.release()

def removeNotFinished():
	for filename in in_progress:
		try:
			os.remove(output_dir + '/' + filename)
		except FileNotFoundError:
			pass

if __name__ == "__main__":
	atexit.register(removeNotFinished)
	parser = argparse.ArgumentParser(description = 'Bing image bulk downloader')
	parser.add_argument('keyword', help = 'Keyword to search')
	parser.add_argument('-o', '--output', help = 'Output directory', required = False)
	parser.add_argument('--filter', help = 'Enable adult filter', action = 'store_true', required = False)
	parser.add_argument('--no-filter', help=  'Disable adult filter', action = 'store_true', required = False)
	args = parser.parse_args()
	if args.output:
		output_dir = args.output
	if adult_filter:
		adlt = ''
	else:
		adlt = 'off'
	if args.no_filter:
		adlt = 'off'
	elif args.filter:
		adlt = ''
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	keyword = args.keyword
	current = 1
	last = ''
	while True:
		response = urllib.request.urlopen('https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keyword) + '&async=content&first=' + str(current) + '&adlt=' + adlt)
		html = response.read().decode('utf8')
		links = re.findall('imgurl:&quot;(.*?)&quot;,oh',html)
		try:
			if links[-1] == last:
				break
			last = links[-1]
			current += bingcount
			for link in links:
				t = threading.Thread(target = download,args = (link,))
				t.start()
		except IndexError:
			print("No search results")
			sys.exit()