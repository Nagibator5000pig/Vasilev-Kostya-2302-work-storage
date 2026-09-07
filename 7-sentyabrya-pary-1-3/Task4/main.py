class Notes:
    uid = 1005435
    title = "Шутка"
    author = "И.С. Бах"
    pages = 2

name_of_author = getattr(Notes, "author")
print(name_of_author)