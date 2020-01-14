import matplotlib.pyplot as plt

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

c_positive_tweets = 0
c_negative_tweets = 0
c_neutral_tweets = 0

pos_words = load_positive_words()
neg_words = load_negative_words()

with open("tweets.txt") as tweet_file:
   tweets = tweet_file.read().splitlines()
   
for tweet in tweets:
    sentiment = sentiment_of_text(tweet);
    if sentiment > 0:
        c_positive_tweets += 1
    elif sentiment < 0:
        c_negative_tweets += 1
    else:
        c_neutral_tweets += 1

labels = ['positive', 'neutral', 'negative']
sentiments = [c_positive_tweets, c_neutral_tweets, c_negative_tweets]
explode = (0.1, 0, 0)  # only "explode" the 1st slice (i.e. 'positive')

fig1, ax1 = plt.subplots()
ax1.pie(sentiments, 
    explode=explode, 
    labels=labels, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=['g', 'w', 'r'],
    wedgeprops = { 'linewidth' : 1, 'edgecolor' : "black"}
)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
     