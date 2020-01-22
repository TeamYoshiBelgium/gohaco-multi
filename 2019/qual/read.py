from domain import *

def read_input(input_file):
    f = open(input_file)
    line = f.readline()
    photos_count = int(line)
    photos = []
    
    index = 0
    for line in f:
        row = line.split(" ")
        orientation = row[0]
        tag_count = row[1]
        tags = row[2:]
        photo = Photo(index, orientation, tags)
        
        photos.append(photo)
        
        index += 1

    f.close()
    
    return photos
