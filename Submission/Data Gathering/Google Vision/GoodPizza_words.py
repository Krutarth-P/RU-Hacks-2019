

import os, shutil
import datetime

now = str(datetime.datetime.now())[:19]
now = now.replace(":","_")
yelp_direct = os.path.join(os.path.dirname(__file__), 'resources/yelp')

out_direct = (os.path.join(os.path.dirname(__file__), 'resources/yelpWord'))

storelist = os.listdir(yelp_direct)

dict = {}

for store in storelist:
    storepath= os.path.join(yelp_direct, str(store))
    files = os.listdir(storepath)
    pics =  [os.path.join(storepath,str(file)) for file in files if  '.jpg' in file]
    if len(pics) > 0:

        txts = [os.path.join(storepath,str(file)) for file in files if  '.txt' in file]
        for txt in txts:
            with open(txt) as f:
                items = f.readlines()
                for item in items:
                    sentence = str(item).split(' ')
                    for word in sentence:
                        if(str(word) != '\\n'):

                            word = str(word.replace('...', ''))
                            word = str(word.replace('?', ''))
                            word = str(word.replace(';', ''))
                            word = str(word.replace('!', ''))
                            word = str(word.replace('"', ''))
                            word = str(word.replace('\\', ''))
                            word = str(word.replace('/', ''))
                            word = str(word.replace('&', ''))
                            word = str(word.replace(',', ''))
                            word = str(word.replace('.', ''))
                            word = str(word.replace(':', ''))
                            word = str(word.replace('\'', ''))
                            word = str(word.replace('(', ''))
                            word = str(word.replace(')', ''))
                            word = str(word.replace(' ', ''))
                            word = str(word.replace('\n', ''))
                            word = str(word.replace('$', ''))
                            word = str(word.replace('\r', ''))
                            word = str(word.replace('*', ''))
                            # print("Original:" + str(word) + " " +str(storepath))
                            if(str(word) is not None and str(word) != '' and word != ''):
                                if(str(word) in dict.keys()):
                                    dict.setdefault(str(word), []).append(pics)
                                else:
                                    dict.setdefault(str(word), []).append(pics)


for key in dict.keys():
    try:
        keydirect = os.mkdir( os.path.join(out_direct, str(key)))
    except Exception as e:
        keydirect =  os.path.join(out_direct, str(key))


    for  list in dict[key]:
        for value in list:
            try:
                basename = os.path.basename(value)

                value3 = os.path.join(keydirect, str(basename))
                value3 = str(basename).replace('.jpg', str(now) + '.jpg')
                print(value3)
                #shutil.copy2(value, value3)

            except Exception as e:
                print(e)
                print("Im dumb couldnt do: " + str(keydirect) + " with key: " + str(key))
                print("Im dumb couldnt do: " + str(value))
