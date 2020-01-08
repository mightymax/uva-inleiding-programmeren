highestPrime = 10000

primeCount = 0 #Keep track of number of primes found so far
number = 1 #Keep track of current number testing for prime

primes = []

while number < highestPrime:
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
            primeCount += 1


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
