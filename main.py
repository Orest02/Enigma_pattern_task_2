from flickr import get_urls
from downloader import download_images
import os
import time
import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import sqlite3


# source: https://medium.com/@adrianmrit/creating-simple-image-datasets-with-flickr-api-2f19c164d82f
# I couldn't download flickrapi from environment file, so I had to install it using 'pip3 install flickrapi', version is 2.4.0

# all_categories = []
# images_total = 100 #actually here per category

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


def init_imgs():
    global all_categories
    print("Is OpenCV Optimized? ", cv2.useOptimized())
    # cv2.setUseOptimized(True) #execute if not optimized

    # Get list of all flickr images

    path = 'data/'
    path = os.path.join(path, all_categories[0])

    images_list = os.listdir(path)
    random.shuffle(images_list)  # shuffle the list of images

    im_list = []

    for im_path in images_list:
        im = cv2.imread(os.path.join(path, im_path))  # read the image from the path
        im_list.append(im)
    return images_list, im_list


def show_img(
        im):  # my version of Opencv can't do imshow and needs remaking, so I will use matplotlib to show the picture
    plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))  # show the colored image after switching from bdr to rgb
    plt.show()


def save_to_sql(df, db_name):
    try:
        sqliteConnection = sqlite3.connect('images.db')
        print("Database created and Successfully Connected to SQLite")

        df.to_sql(name=db_name, con=sqliteConnection, if_exists='replace')  # , dtype={'Greyscaled':'BLOB'})
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def retrieve_from_db(query):
    try:
        sqliteConnection = sqlite3.connect('images.db')
        print("Database created and Successfully Connected to SQLite")

        new_df = pd.read_sql(sql=query, con=sqliteConnection)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        new_df = None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return new_df


if __name__ == '__main__':
    arg_list = sys.argv
    all_categories = []
    images_total = 100
    # global all_categories, images_total
    for i, arg in enumerate(arg_list):
        if i == 1:
            all_categories.append(str(arg))
        if i == 2:
            if RepresentsInt(arg):
                images_total = int(arg)
            else:
                print('The argument passed as numbe rof images isn\'t integer\n')

    start_time = time.time()

    download()

    images_list, im_list = init_imgs()

    show_img(im_list[0])  # show first image

    # put data in sqlite. For this purpose I will make use of pandas built-in functions

    df = pd.DataFrame(im_list, columns=['Images'])

    save_to_sql(df, 'Flickr')

    print('Took {} seconds'.format(round(time.time() - start_time, 2)))
