# Name: Mark Lindeman
# Collaborators: Mees Lindeman
#
# This program proves Goldbach’s conjecture to be true for all even numbers up to and including 1000.
# see https://progbg.mprog.nl/numbers/goldbach

number = 1 #Keep track of current number testing for prime
primes = []
maxNumber = 1000

while number < maxNumber:
    number = number + 1
    z = 0
    for i in range(2, number):
        if (number % i) == 0:
            # not a prime
            z = z + 1

    if z == 0:
        primes.append(number)

prove = 0
for i in range(4, maxNumber + 1, 2):
    for prime in primes:
        if (i - prime) in primes:
            print(f"{i} = {prime} + {i - prime}")
            prove = 1
            break
    if prove == 0:
        print(f"Goldback was wrong, {i} can not be expressed as the sum of two primes.")
