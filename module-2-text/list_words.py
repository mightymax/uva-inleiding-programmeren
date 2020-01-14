source_text = "The apple doesn't fall far from the tree."

def cleanup(word):
    cleaned = word.rstrip(' .')
    return cleaned.lower()

def text_to_unique_words(text):
    unique_words = []
    words = text.split()
    for word in words:
        word = cleanup(word)
        if word not in unique_words:
            unique_words.append(word)
    unique_words.sort()
    return unique_words
    
print(text_to_unique_words(source_text))