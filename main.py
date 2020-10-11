from flickr import get_urls
from downloader import download_images
import os
import time
import sys


#source: https://medium.com/@adrianmrit/creating-simple-image-datasets-with-flickr-api-2f19c164d82f
#I couldn't download flickrapi from environment file, so I had to install it using 'pip3 install flickrapi', version is 2.4.0

#all_categories = []
#images_total = 100 #actually here per category

def download():
    global all_categories, images_total
    if not all_categories:
        all_categories = ['recent']
    for category in all_categories:

        print('Getting urls for: ', category)
        urls = get_urls(category, images_total)

        print('Downloading images for: ', category)
        path = os.path.join('data', category)

        download_images(urls, path)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ =='__main__':
    arg_list = sys.argv
    all_categories = []
    images_total = 100
    #global all_categories, images_total
    for i,arg in enumerate(arg_list):
        if i==1:
            all_categories.append(str(arg))
        if i==2:
            if RepresentsInt(arg):
                images_total = int(arg)
            else:
                print('The argument passed as numbe rof images isn\'t integer\n')

    start_time = time.time()

    download()

    print('Took {} seconds'.format(round(time.time() - start_time, 2)))
