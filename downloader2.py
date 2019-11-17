import requests
from time import time as timer
from multiprocessing.pool import ThreadPool
import threading
import click
import math

def Handler(start,end,url,filename):
	headers = {'Range': 'bytes=%d-%d' % (start, end)} 
  
	# request the specified part and get into variable     
	r = requests.get(url, headers=headers, stream=True)
  
	# open the file and write the content of the html page  
	# into file. 
	# if r.status_code == 200:
	# 	with open(filename, 'wb') as f:
	# 		for chunk in r.iter_content(chunk_size=8092):
	# 					if chunk:
	# 						f.write(chunk)
	with open(filename, "r+b") as fp:
		for chunk in r.iter_content(chunk_size=8092):
			fp.seek(start) 
			var = fp.tell() 
			fp.write(r.content)
	  
		


# def fetch_url(entry):
# 	#split:
# 	path, uri = entry
# 	if not os.path.exists(path):
# 		r = requests.get(uri, stream=True)
# 		if r.status_code == 200:
# 			with open(path, 'wb') as f:
# 				for chunk in r.iter_content(chunk_size=8092):
# 					if chunk: 
# 						f.write(chunk)
# 	return path
	

@click.command(help="It downloads the specified file with specified name") 
@click.option('--number_of_threads',default=1, help="No of Threads")
@click.option('--name',type=click.Path(),help="Name of the file with extension") 
@click.argument('url_of_file',type=click.Path()) 
@click.pass_context
def download_file(ctx,url_of_file,name,number_of_threads): 
	begTime = timer()
	r = requests.head(url_of_file) 
	if name: 
		file_name = name 
	else: 
		file_name = url_of_file.split('/')[-1] 
	try: 
		file_size = int(r.headers['content-length'])
	except: 
		print "Invalid URL"
		return
	
	part = int(file_size) // number_of_threads
	# The integer split might not occur evenly, in which case the part size has to be increased to match
	# the original file size
	if (file_size % number_of_threads != 0):
		part = part + 1
	part = math.ceil(part)
	fp = open(file_name, "wb") 
	fp.write(b'\0' * file_size) 
	fp.close()
	for i in range(number_of_threads): 
		start = part * i 
		end = start + part
		if (end == file_size - 1):
			end = file_size
		  # create a Thread with start and end locations 
		t = threading.Thread(target=Handler, 
			   kwargs={'start': start, 'end': end, 'url': url_of_file, 'filename': file_name}) 
		t.setDaemon(True) 
		t.start() 

	main_thread = threading.current_thread()
	for t in threading.enumerate(): 
		if t is main_thread:
			continue
		t.join()
	print ('%s downloaded' % file_name)

	elapsed_time = timer() - begTime

	print("Elapsed Time: ")
	print(elapsed_time)
#to do: create test bash commands and a folder for it
#test using: https://www.thinkbroadband.com/download
#put on github

if __name__ == '__main__': 
	#threads run in the same memory space and therefore multiple threads may be writing to the same memory simultaneously
	#spawning processes is a little slower, however they will not write to the same memory space
	#default number of threads is 1, if the file is too small a large amount of threads breaks the download
	download_file(obj={})



