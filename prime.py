nthPrime = 0
while nthPrime < 1:
    nthPrime = input("Which prime number are you looking for? ")
    nthPrime = int(nthPrime)

primeCount = 0 #Keep track of number of primes found so far
number = 1 #Keep track of current number testing for prime

while primeCount < nthPrime:
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
            primeCount = primeCount + 1

print(f"{number}")