import io
import os
from PIL import Image, ImageDraw
import shutil

from google.cloud import vision
from google.cloud.vision import types
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Tudor\\IdeaProjects\\GoodPizza-3f5e11a16d21.json"
client = vision.ImageAnnotatorClient()

dirs_input =  os.listdir( os.path.join(os.path.dirname(__file__), 'resources/Input'))
dirs_output =  os.path.join(os.path.dirname(__file__), 'resources/Output')

for dirsIn in dirs_input:
    file_input = os.path.join(os.path.join(os.path.dirname(__file__), 'resources/Input'), str(dirsIn))
    files = os.listdir(file_input)
    file_output = os.path.join( dirs_output, str(dirsIn))
    outputlist = []
    print("exploring Files in: " + str( file_input) )
    for file in files:
        filepath =  str(file_input) + '/' + str(file)
        try:
            with io.open(filepath, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            response = client.label_detection(image=image)

            labels = response.label_annotations
            for label in labels:
                if label.description == "Pizza":
                    outputlist.append(filepath)

        except:
            print("Error opening file: " + str(filepath))

    print("outputting Files in: " + str( file_output) )
    for file in outputlist:
        shutil.copy2(file, file_output)


file_input = os.path.join(os.path.dirname(__file__), 'resources/Good Pizza Input')
files = os.listdir(file_input)
file_output = os.path.join( os.path.join(os.path.dirname(__file__), 'resources/Good Pizza Output'))
outputlist = []


for file in files:
    filepath =  str(file_input) + '/' + str(file)
    try:
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.label_detection(image=image)

        labels = response.label_annotations
        for label in labels:
            if label.description == "Pizza":
                outputlist.append(filepath)

    except:
        print("Error opening file: " + str(filepath))

print(outputlist)
for file in outputlist:
    filepath =  str(file_input) + '/' + str(file)
    shutil.copy2(file, file_output)
