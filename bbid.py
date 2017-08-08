#!/usr/bin/env python3
import os, sys, urllib.request, urllib.error, re, threading, posixpath, urllib.parse, argparse, random, socket, time, hashlib, pickle, signal, imghdr

#config
output_dir = './bing' #default output dir
adult_filter = True #Do not disable adult filter by default
pool_sema = threading.BoundedSemaphore(value = 20) #max number of download threads
bingcount = 35 #default bing paging
limit = 10 #default nb results limit
socket.setdefaulttimeout(2)

in_progress = {}
tried_urls = []
image_md5s = {}
urlopenheader={ 'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
def download(url,output_dir):
	search_id = output_dir.split('/')[-1]
	if search_id not in in_progress:
		in_progress[search_id] = []
	if url in tried_urls or len(os.listdir(output_dir)) + len(in_progress[search_id]) > limit:
		return
	pool_sema.acquire()
	path = urllib.parse.urlsplit(url).path
	filename = posixpath.basename(path).split('?')[0] #Strip GET parameters from filename
	name, ext = os.path.splitext(filename)
	name = name[:36]
	filename = name + ext
	i = 0
	while os.path.exists(os.path.join(output_dir, filename)) or filename in in_progress[search_id]:
		i += 1
		filename = "%s-%d%s" % (name, i, ext)
	in_progress[search_id].append(filename)

	try:
		request=urllib.request.Request(url,None,urlopenheader)
		image=urllib.request.urlopen(request).read()

		if not imghdr.what(None, image):
			print('FAIL: Invalid image, not saving ' + filename)
			return

		md5_key = hashlib.md5(image).hexdigest()
		if md5_key in image_md5s:
			print('FAIL: Image is a duplicate of ' + image_md5s[md5_key] + ', not saving ' + filename)
			return

		nb_files = len(os.listdir(output_dir))
		if nb_files >= limit:
			return

		image_md5s[md5_key] = filename
		imagefile=open(os.path.join(output_dir, filename),'wb')
		imagefile.write(image)
		imagefile.close()
		print('OK ("%s" %d/%d): %s' % (search_id, nb_files+1, limit, filename))
		tried_urls.append(url)
	except urllib.error.HTTPError as e:
		print("FAIL (HTTPError): %s: %s" % (filename, e))
	except urllib.error.URLError as e:
		print("FAIL (URLError): %s: %s" % (filename, e))
	except socket.timeout as e:
		print("FAIL (timeout): %s: %s" % (filename, e))

	finally:
		in_progress[search_id].remove(filename)
		pool_sema.release()

def fetch_images_from_keyword(keyword,output_dir):
	current = 1
	links = []
	while len(links)<=limit*2: # We except at last 50% of valid images.
		request_url='https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(keyword) + '&async=content&first=' + str(current) + '&adlt=' + adlt
		request=urllib.request.Request(request_url,None,headers=urlopenheader)
		response=urllib.request.urlopen(request)
		html = response.read().decode('utf8')
		links += re.findall('murl&quot;:&quot;(.*?)&quot;',html)
		try:
			current += bingcount
			for link in links:
				t = threading.Thread(target = download,args = (link,output_dir))
				t.start()
		except IndexError:
			print('No search results for "{0}"'.format(keyword))
			return
		time.sleep(0.1)

def backup_history(*args):
	download_history = open(os.path.join(output_dir, 'download_history.pickle'), 'wb')
	pickle.dump(tried_urls,download_history)
	copied_image_md5s = dict(image_md5s)  #We are working with the copy, because length of input variable for pickle must not be changed during dumping
	pickle.dump(copied_image_md5s, download_history)
	download_history.close()
	print('history_dumped')
	if args:
		exit(0)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Bing image bulk downloader')
	parser.add_argument('-s', '--search-string', help = 'Keyword to search', required = False)
	parser.add_argument('-f', '--search-file', help = 'Path to a file containing search strings line by line', required = False)
	parser.add_argument('-o', '--output', help = 'Output directory', required = False)
	parser.add_argument('-l', '--limit', type = int, help = 'Number of results limit', required = False)
	parser.add_argument('--filter', help ='Enable adult filter', action = 'store_true', required = False)
	parser.add_argument('--no-filter', help = 'Disable adult filter', action = 'store_true', required = False)
	args = parser.parse_args()
	if (not args.search_string) and (not args.search_file):
		parser.error('Provide Either search string or path to file containing search strings')
	if args.output:
		output_dir = args.output
	if args.limit:
		limit = args.limit
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	output_dir_origin = output_dir
	signal.signal(signal.SIGINT, backup_history)
	try:
		download_history = open(os.path.join(output_dir, 'download_history.pickle'), 'rb')
		tried_urls=pickle.load(download_history)
		image_md5s=pickle.load(download_history)
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
	if args.search_string:
		fetch_images_from_keyword(args.search_string,output_dir)
	elif args.search_file:
		try:
			inputFile=open(args.search_file)
		except (OSError, IOError):
			print("Couldn't open file {}".format(args.search_file))
			exit(1)
		for keyword in inputFile.readlines():
			output_sub_dir = os.path.join(output_dir_origin, keyword.strip().replace(' ', '_'))
			if not os.path.exists(output_sub_dir):
				os.makedirs(output_sub_dir)
			fetch_images_from_keyword(keyword,output_sub_dir)
			backup_history()
		inputFile.close()
