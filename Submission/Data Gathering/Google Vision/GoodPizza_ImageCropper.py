import io
import os
from PIL import Image, ImageDraw
import shutil

from google.cloud import vision
from google.cloud.vision import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Tudor\\IdeaProjects\\GoodPizza-3f5e11a16d21.json"


yelp_direct = os.path.join(os.path.dirname(__file__), 'resources/yelp')



storesIn = os.listdir(yelp_direct)








def cropImage (imagepath):


    client = vision.ImageAnnotatorClient()
    hints = None
    try:
        with io.open(imagepath, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        image_context = types.ImageContext()

        response = client.label_detection(image=image)


        labels = response.label_annotations
        hints = None
        for label in labels:
            if label.description == "Pizza":
                response2 = client.crop_hints(image=image, image_context= image_context)
                hints = response2.crop_hints_annotation.crop_hints

    except:
        print("Error opening file: " + str(imagepath))
        return None

    if(hints is not None):
        print(hints)
        verticies = hints[0].bounding_poly.vertices
    else:
        verticies = None
        os.remove(imagepath)

    return verticies

def crop_to_hint(image_file, outputFile):
    """Crop the image using the hints in the vector list."""
    vects = cropImage(image_file)
    if(vects is not None):
        im = Image.open(image_file)
        im2 = im.crop([vects[0].x, vects[0].y,
                       vects[2].x - 1, vects[2].y - 1])
        im2.save(str(outputFile))
        print('Saved new image to ' + str(outputFile))
    else : print("No Crop Made No File Saveed")
    return


for store in storesIn:
    storepath = os.path.join(yelp_direct, str(store))
    reviews = os.listdir(str( storepath))

    for review in reviews:
        if ('txt' in  str(review)):
            print("Text")
        else:
            print('image ' + str(review))
            imagepath = os.path.join(storepath, str(review))
            outputfile = os.path.join(storepath, 'crop-'+str(review))
            crop_to_hint(imagepath, outputfile)
