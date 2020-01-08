highestPrime = 10000

primeCount = 0 #Keep track of number of primes found so far
number = 1 #Keep track of current number testing for prime

primes = []

while number < highestPrime:
    number = number + 1
    
    z = 0
    for i in range(2, number):
        if (number % i) == 0:
            # not a prime
            z = z + 1

    if z == 0:
        primeCount = primeCount + 1
        primes.append(number)
    
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
