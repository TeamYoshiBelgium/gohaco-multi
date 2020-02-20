import math


class Library:
    CNTR = 0

    def __init__(self, O, books_count, signup, rate, books):
        self.O = O

        self.done = False
        self.books_count = books_count
        self.rate = rate
        self.signup = signup
        self.books = books

        self.days_needed = math.ceil(self.books_count * 1.0 / self.rate)
        self.book_score = self.get_book_score()

    def get_score(self):
        signup_score = -self.signup
        book_score = self.get_book_score()
        length_score = -self.days_needed
        rate_score = self.rate
        score = signup_score + book_score + length_score + rate_score
        return score

    def get_book_score(self):
        book_score = 0
        for book in self.books:
            book_score += book.get_score()
        return book_score
