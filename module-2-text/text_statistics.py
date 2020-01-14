source_text = "ASDF is the sequence of letters that appear on the first four keys on the home row of a QWERTY or QWERTZ keyboard. They are often used as a sample or test case or as random, meaningless nonsense. It is also a common learning tool for keyboard classes, since all four keys are located on Home row." # from the wikipedia

def number_of_letters_in(text):
    c = 0
    for char in text:
        if char.isalpha():
            c += 1
    return c
    
def number_of_words_in(text):
    words = text.split()
    return len(words)

def number_of_sentences_in(text):
    # remove all DOTS/SPACES from end of text, no need to split on the end of the sentence:
    text = text.rstrip(' .')
    sentences = text.split('.')
    return len(sentences)

def average_word_length(text):
    words = text.split()
    c = 0
    for word in words:
        c += len(word)
    return round(c / len(words), 2)
    

print(source_text)
print(number_of_letters_in(source_text))
print(number_of_words_in(source_text))
print(number_of_sentences_in(source_text))
print(average_word_length(source_text))
