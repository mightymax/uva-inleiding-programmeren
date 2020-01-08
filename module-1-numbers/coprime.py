# Name: Mark Lindeman
#
# program that calculates the chance that two random whole numbers do not have a common divisor. Such a pair of numbers is called a coprime.
# see https://progbg.mprog.nl/numbers/co-primes

import random

def prime_factors(number):
    factors = []
    
    i = number
    while i > 1:
        for prime in primes:
            if i % prime == 0:
                factors.append(prime)
                i = i / prime
    factors.sort()
    return factors
    
def divisor_count(n1, n2):
    prime_factors_n1 = prime_factors(n1)
    prime_factors_n2 = prime_factors(n2)

    for n in prime_factors_n1:
        if n in prime_factors_n2:
            return 1

    for n in prime_factors_n2:
        if n in prime_factors_n1:
            return 1

    return 0
    
def get_primes(n_max):
    number = 1 #Keep track of current number testing for prime

    primes = []

    while number < n_max:
        number = number + 1
        if (number == 2 or number % 2 != 0): #test only uneven numbers and 2
            count = 0 #Keep track of itteration count, need this to see if we tested all combinations

            #loop thru all integers using steps of 2, no need to test even numbers
            for x in range(3, number, 2):
                if (number % x) == 0:
                    #Number {number} is not a prime
                    break

                #increase counter by 2 because of loop steps is also 2:
                count = count + 2

            if (count + 3 == number or number == 2):
                #Number is a prime so add one to primeCount
                primes.append(number)
    
    return primes
    
def experiment(n_min = 10000, n_max = 100000, max_pairs = 10000):
    c = 0
    i = 0
    while i < max_pairs:
        n1 = random.randint(n_min, n_max)
        n2 = random.randint(n_min, n_max)
        c += divisor_count(n1, n2)
        i += 1
        
    fraction = c / max_pairs
    return fraction


def prediction(n):
    #TODO: Write a function prediction(n) that predicts the theoretical chance of n numbers having no common divisors. This consists of not much more than calculating the Riemann zeta function yourself and with that determine the correct chance.
    fraction = 0.666
    return fraction
    

n_min = 1000 #* 10
n_max = 10000 #* 10
max_pairs = 10000

#Global var primes, used in functions
primes = get_primes(n_max)

print("The chance that two random numbers do not share a common divisor is:")
print("    - prediction (mathematical): %0.3f" % prediction(1))
print("    - empirical (Python): %0.3f" % experiment(n_min, n_max, max_pairs))