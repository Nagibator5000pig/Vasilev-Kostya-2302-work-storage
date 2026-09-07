class Dictionary:
    rus = "Питон"
    eng = "Python"

word = getattr(Dictionary, "rus_word", False)
print(word)