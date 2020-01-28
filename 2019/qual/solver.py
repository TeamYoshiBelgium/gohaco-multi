from domain import *
from tqdm import tqdm

# 4
# --- 0.0 seconds ---
# in/a_example.txt Score: 1 of max score: -1
# 80000
# --- 0.8702256679534912 seconds ---
# in/b_lovely_landscapes.txt Score: 12 of max score: -1
# 1000
# --- 0.0 seconds ---
# in/c_memorable_moments.txt Score: 174 of max score: -1
# 90000
# --- 0.7345876693725586 seconds ---
# in/d_pet_pictures.txt Score: 191163 of max score: -1
# 80000
# --- 0.9698977470397949 seconds ---
# in/e_shiny_selfies.txt Score: 112617 of max score: -1
# Total score: 303967
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

def find_solution_2(photos_dict):
    slideshow = []

    slides = {}

    key_list = sorted(photos_dict['H'].keys(), reverse=True)

    for tags_count in key_list:
        if tags_count not in slides:
            slides[tags_count] = []
        slide_list = slides[tags_count]

        photo_per_tag = photos_dict['H'][tags_count]
        for photo in photo_per_tag:
            slide = Slide([photo])
            slide_list.append(slide)

    photos_v = []
    key_list = sorted(photos_dict['V'].keys(), reverse=True)

    for tags_count in key_list:
        if tags_count not in slides:
            slides[tags_count] = []
        slide_list = slides[tags_count]

        photos_v += photos_dict['V'][tags_count]

        while len(photos_v) > 1:
            photo_1 = photos_v.pop()
            photo_2 = photos_v.pop()
            slide = Slide([photo_1, photo_2])

            if slide.tags_count in slides:
                slides[slide.tags_count].append(slide)
            else:
                slides[slide.tags_count] = [slide]

    key_list = sorted(slides.keys(), reverse=True)
    for tags_count in tqdm(key_list):
        result = optimize(slides[tags_count])
        slideshow += result

    return slideshow

def optimize(slides):
    sorted = []
    if len(slides) == 0:
        return sorted

    if len(slides) > 2000:
        print(len(slides))
        return slides

    slide_a = slides.pop()
    sorted.append(slide_a)

    while(len(slides) >= 1):
        best_score = 0
        best_index = 0
        index = -1
        for slide_b in slides:
            index += 1
            score = slide_a.get_score(slide_b)
            if(best_score < score):
                best_score = score
                best_index = index

        slide_a = slides.pop(best_index)
        sorted.append(slide_a)

    return sorted