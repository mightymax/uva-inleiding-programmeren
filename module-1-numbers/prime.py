nthPrime = 0
while nthPrime < 1:
    nthPrime = input("Which prime number are you looking for? ")
    nthPrimeAsFloat = float(nthPrime)
    nthPrime = int(nthPrimeAsFloat)
    if nthPrimeAsFloat - nthPrime > 0:
        nthPrime = 0

primeCount = 0 #Keep track of number of primes found so far
number = 1 #Keep track of current number testing for prime

while primeCount < nthPrime:
    number = number + 1
    z = 0
    for i in range(2, number):
        if (number % i) == 0:
            # not a prime
            z = z + 1

    if z == 0:
        primeCount = primeCount + 1

print(f"{number}")