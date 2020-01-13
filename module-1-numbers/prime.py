nthPrime = 0
while nthPrime < 1:
    nthPrime = input("Which prime number are you looking for? ")
    nthPrimeAsFloat = float(nthPrime)
    nthPrime = int(nthPrimeAsFloat)
    if nthPrimeAsFloat - nthPrime > 0:
        nthPrime = 0


# start primeCount with '1', since 2 is a prime
primeCount = 1
number = 1

while primeCount < nthPrime:
    c = 0
    if (number > 1):
        for i in range(2, number):
            if (c < 1):
                if number % i == 0:
                    c = c + 1

    if c == 0 and number > 1:
        primeCount += 1

    # increase loop by 2, even numbers are never primes
    number += 2

#end of the loop: number - 2 is now the prime we are looking for, see while loop
print(number - 2)
