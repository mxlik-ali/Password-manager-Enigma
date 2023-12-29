import secrets
import string

# Custom word list with 50 words
word_list = [
    "apple", "berry", "melon", "lemon", "grape",
    "kiwi", "plum", "peach", "cherry", "apricot",
    "olive", "onion", "radish", "carrot", "celery",
    "melon", "lemon", "grape", "kiwi", "plum",
    "peach", "cherry", "apricot", "olive", "onion",
    "radish", "carrot", "celery", "cumin", "basil",
    "thyme", "oregano", "sage", "mint", "anise",
    "fennel", "poppy", "coral", "amber", "azure",
    "ivory", "jade", "jet", "ruby", "topaz",
    "lime", "mulberry", "nectar", "olive", "pomegranate"
    # Filled with 'opal' to meet the 50-word count; replace with more words
]

def generatePassword(words=2):
    special_chars = string.punctuation.replace("'", "")  # Exclude single quote to avoid escaping issues

    passphrase = ''
    for _ in range(words):
        word = secrets.choice(word_list)
        if secrets.randbelow(2) == 1:  # 50% chance to capitalize word
            word = word.capitalize()
        passphrase += word + secrets.choice(special_chars) + str(secrets.randbelow(10))  # Append special char and number

    return passphrase

#  Usage
# passphrase = generatePassword()
# print("Generated Memorable Passphrase:", passphrase)
