from domain import *

def read_input(input_file):
    f = open(input_file)
    line = f.readline()
    photos_count = int(line)
    photos = []
    photos_dict = {}
    photos_dict['H'] = {}
    photos_dict['V'] = {}

    index = 0
    for line in f:
        row = line.strip().split(" ")
        orientation = row[0]
        tag_count = int(row[1])
        tags = [x.strip() for x in row[2:]]
        photo = Photo(index, orientation, tags)
        
        photos.append(photo)

        if tag_count in photos_dict[photo.orientation]:
            photos_dict[photo.orientation][tag_count].append(photo)
        else:
            photos_dict[photo.orientation][tag_count] = [photo]

        index += 1

    f.close()
    return photos, photos_dict
