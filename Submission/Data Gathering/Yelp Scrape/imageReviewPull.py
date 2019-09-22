import urllib.request
import os
from yelpapi import YelpAPI
yelp_api = YelpAPI("vr5j0WwPWclnATJzHjssNFVwlbMNWvW13Ksc7pYyI7VDoaRQl98tAxlRmglJk2Cd3uouxCZxN6QgFCX4P5JNFzKflvbRlbNnnDrbi-GfvyxPBheDfN6EErECpEPgXHYx")
search_results = yelp_api.search_query(term='Pizza', location='Halifax', sort_by='rating', limit=50)

businessIds = list()
businessRating = list()
#businessPhotos = list()
#businessReviews = list()

for result in search_results["businesses"]:
    businessIds.append(result["id"])
    businessRating.append(result["rating"])

for businessId in businessIds:
    businessPhotos = yelp_api.business_query(id=businessId)["photos"]
    businessReviews = yelp_api.reviews_query(id=businessId)["reviews"]

    os.mkdir(businessId)
    i = 0
    for photo in businessPhotos:
        savefile = str(businessId + "/" + str(i) + ".jpg")
        urllib.request.urlretrieve(photo, savefile)
        i = i + 1
    
    i = 0
    for review in businessReviews:
        savefile = str(businessId + "/" + str(i) + ".txt")
        fsavefile = open(savefile, "w")
        fsavefile.write(review["text"])
        i = i + 1