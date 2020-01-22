from domain import *


def find_solution(photos):
    slideshow = []
    slide_photos_vertical = []

    photos_v = []
    photos_h = []
    for photo in photos:
        if(photo.orientation == 'H'):
            photos_h.append(photo)
        elif(photo.orientation == 'V'):
            photos_v.append(photo)
        else:
            raise Exception

    while len(photos_v) > 1:
        photo_v = photos_v.pop()
        max_tag_count = 0
        max_tag_photo_index = 0
        photo_index = 0
        # for other in photos_v:
        #     tag_count = len(photo_v.tags.intersection(other.tags))
        #     if(tag_count > max_tag_count):
        #         max_tag_photo_index = photo_index
        #     photo_index += 1

        other = photos_v.pop(max_tag_photo_index)

        slide = Slide([photo_v, other])
        slideshow.append(slide)

    for photo in photos_h:
        slide = Slide([photo])
        slideshow.append(slide)

    return slideshow
