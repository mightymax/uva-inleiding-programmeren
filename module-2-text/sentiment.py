def load_words(filename):
    content = open(filename)
    lines = content.read().splitlines()
    content.close()
    return lines

def load_positive_words():
    return load_words("pos_words.txt")

def load_negative_words():
    return load_words("neg_words.txt")

def cleanup(word):
    cleaned = word.rstrip(' .')
    return cleaned.lower()

pos_words = load_positive_words()
neg_words = load_negative_words()

def sentiment_of_word(word):
    word = cleanup(word)
    if word in neg_words:
        return -1
    if word in pos_words:
        return 1
    return 0
    
def sentiment_of_text(text):
    sentiment = 0
    words = text.split()
    for word in words:
        sentiment += sentiment_of_word(word);
    return sentiment

total_score = sentiment_of_text("Pastel-colored 1980s day cruisers from Florida are ugly.")
print(total_score)
# if total_score > 0:
#     print("The text is mostly nice!")
# elif total_score < 0:
#     print("The text talks about mad or bad stuff :(")
# else:
#     print("The text is not opinionated or just messy.")
