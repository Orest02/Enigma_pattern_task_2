from flickrapi import FlickrAPI
from api_keys import api_keys

KEY, SECRET = api_keys()

SIZES = ["url_o", "url_k", "url_h", "url_l", "url_c"]  # in order of preference

#we can do the search using “flickr.walk” which returns an iterable object
#for recent photos i could use flickr.do_flickr_call bc there's no function for recent photos and new api doesn't support parameterless search of photos, so i had to use this time 'recent'  as a keyword

def get_photos(image_tag):
    extras = ','.join(SIZES)
    flickr = FlickrAPI(KEY, SECRET)
    #if image_tag != 'recent':
    photos = flickr.walk(text=image_tag,  # it will search by image title and image tags
            extras=extras,  # get the urls for each size we want
            privacy_filter=1,  # search only for public photos
            per_page=50,
            sort='relevance')  # we want what we are looking for to appear first
    #else:
    #    photos = flickr.do_flickr_call(flickr.photos.getRecent(api_key=KEY))
    return photos

#this function will allow us to get the URL for a photo following our list of sizes.

def get_url(photo):
    for i in range(len(SIZES)): #Makes sure the loop is done in the order we want
        url = photo.get(SIZES[i])
        if url: #if url is None try next size
            return url

#Putting those two functions together we can get all the images we want with the desired size.

def get_urls(image_tag, Max):
    photos = get_photos(image_tag)
    counter=0
    urls=[]

    for photo in photos:
        if counter < Max:
            url = get_url(photo)  # get preffered size url
            if url:
                urls.append(url)
                counter += 1
            # if no url for the desired sizes then try with the next photo
        else:
            break

    return urls

