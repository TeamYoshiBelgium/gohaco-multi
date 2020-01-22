import os

def write_solution(slideshow, filename):
    if not os.path.isdir("output"):
        os.mkdir("output")
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(slideshow)))
    f.write("\n")
    for slide in slideshow:
        for photo in slide.photos:
            f.write(str(photo.id) + " ")
        f.write("\n")
    f.close()
