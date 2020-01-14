# Exercises from https://progbg.mprog.nl/text/strings (Looping with strings)

print ("Exercise 1: reversed loop thru string:")
myString = "Lorum Ipsum" 

index = len(myString) - 1
while index >= 0:
    letter = myString[index]
    print(letter)
    index = index - 1
    
print ("Exercise 2: reversed loop thru string:")
prefixes = 'JKLMNOPQ'
suffix = 'ack'

for letter in prefixes:
    if letter in 'OQ':
        extraLetter = 'u'
    else:
        extraLetter = ''    
    print(letter + extraLetter + suffix)

# Exercise — There is a string method called count that is similar to the function count above. Read the documentation of this method and write an invocation that counts the number of as in 'banana'.

fruit = 'banana'
count_char = 'a'
print (f"Exercise 3: using str.count(\'{count_char}\') method on string \'{fruit}\'")
print(fruit.count(count_char))

