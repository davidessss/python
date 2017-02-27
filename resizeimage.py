from PIL import Image
import os
import errno
import shutil
import glob
import sys
import logging

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
        
def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def removedirtree(file_path):
    for root, dirs, files in os.walk(file_path):
        if root != file_path:
            shutil.rmtree(root)
            print "delete: " + root
        else:
            r = glob.glob(root+"/*.*")
            for i in r:
                os.remove(i)
                print "delete file: " + i


logger = logging.getLogger('resizeimage')
hdlr = logging.FileHandler('resizeimage.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

size = 800, 800
directory = "/volume1/Dati/Immagini/2016"
dirthumb = "/volume1/photo"
removedirtree(dirthumb)


for root, dirs, files in os.walk(directory):
    print"***********************************"
	dimensione = convert_bytes(getFolderSize(root))
    print root + " - " + dimensione
	logger.info(root + " - " + dimensione)
    newdir = root.replace(directory,dirthumb)
    if root != directory:
        print "mkdir: " + newdir
        make_sure_path_exists(newdir)
    numfile = 0
    for filename in os.listdir(root):
        if filename.lower().endswith(".jpg"):
			try:
				infile = os.path.join(root, filename)
				im = Image.open(infile)
				im.thumbnail(size)
				im.save(newdir + "/" + filename, "JPEG")
				print infile
				print newdir + "/" + filename
				numfile = numfile + 1
			except:
				messaggio = "errore di conversione al file %s" % infile
				print messaggio
				logger.error(messaggio)
    print "convertiti %s file" % numfile
	logger.info("convertiti %s file" % numfile)
            

            
