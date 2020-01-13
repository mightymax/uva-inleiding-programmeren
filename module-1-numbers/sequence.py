# start primeCount with '1', since 2 is a prime
highestPrime = 10000
primeCount = 1
number = 1
primes = [2]


while number < highestPrime:
    c = 0
    if (number > 1):
        for i in range(2, number):
            if (c < 1):
                if number % i == 0:
                    c = c + 1

    if c == 0 and number > 1:
        primeCount += 1
        primes.append(number)

    # increase loop by 2, even numbers are never primes
    number += 2

max_length = 0
min_prime = 0
max_prime = 0

ix = 0
for prime in primes:
    if ix+1 < primeCount and primes[ix+1] - prime > max_length:
        max_length = primes[ix+1] - prime
        min_prime = prime
        max_prime = primes[ix+1]
    ix += 1
    
print(f"The longest sequence non-primes under {highestPrime} starts at {min_prime+1} and ends at {max_prime-1}")
print(f"The sequence is {max_length-1} long.")
