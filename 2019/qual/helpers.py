def score_max(photos):
    return -1


def validate_solution(slideshow):
    # print(pizzas)
    photo_ids = set()
    for slide in slideshow:
        if(len(slide.photos) == 1):
            if(slide.photos[0].orientation != "H"):
                return False
        elif(len(slide.photos) == 2):
            if(slide.photos[0].orientation != "V"):
                return False
            elif(slide.photos[1].orientation != "V"):
                return False
        else:
            return False

        ids = [photo.id for photo in slide.photos]
        not_unique_ids = photo_ids.intersection(ids)
        if len(not_unique_ids) != 0:
            print(not_unique_ids)
            return False
        photo_ids.update(ids)
    return True


def calculate_score(slideshow):
    score = 0
    if not validate_solution(slideshow):
        return -1
    length = len(slideshow)
    if length == 0:
        return score

    prev_slide = slideshow[0]
    for index in range(1, length):
        current_slide = slideshow[index]
        score += prev_slide.get_score(current_slide)
        prev_slide = current_slide
    return score


def print_mat(mat):
    for row in mat:
        for cell in row:
            if cell > 9:
                print("" + str(cell) + " ", end="")
            elif cell > 0:
                print(" " + str(cell) + " ", end="")
            else:
                print("" + str(cell) + " ", end="")
        print()
