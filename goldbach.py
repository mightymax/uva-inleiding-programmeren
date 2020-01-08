number = 1 #Keep track of current number testing for prime
primes = []
maxNumber = 1000

while number < maxNumber:
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
            #Number is a prime so add one to prime_count
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
