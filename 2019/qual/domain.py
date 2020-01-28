class Photo:
    def __init__(self, id, orientation, tags):
        self.id = id
        self.orientation = orientation
        self.tags = set(tags)

    def __str__(self):
        string = "id: %i orientation: %s tags: %s\n" % (self.id, self.orientation, str(self.tags))
        return string
        
    def __repr__(self):
        string = "id: %i orientation: %s tags: %s" % (self.id, self.orientation, str(self.tags))
        return string

class Slide:

    def __init__(self, photos):
        self.photos = photos
        self.tags = set()
        for photo in photos:
            for tag in photo.tags:
                self.tags.add(tag)

        self.tags_count = len(self.tags)

    def get_score(self, other):
        intersection = len(self.tags.intersection(other.tags))
        difference_self = len(self.tags.difference(other.tags))
        difference_other = len(other.tags.difference(self.tags))
        score = min(intersection, difference_self, difference_other)
        # print("intersection: %i difference_self: %i difference_other: %i score: %i"
        #      % (intersection, difference_self, difference_other, score))

        return score