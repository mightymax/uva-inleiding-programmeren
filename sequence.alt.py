highestPrime = 10000
number = 1 #Keep track of current number testing for prime
nonPrimes = []

while number < highestPrime:
    number = number + 1
    if (number == 2 or number % 2 != 0): #test only uneven numbers and 2
        #loop thru all integers using steps of 2, no need to test even numbers
        for x in range(3, number, 2):
            if (number % x) == 0:
                #Number {number} is not a prime
                nonPrimes.append(number)
                break
    else:
        nonPrimes.append(number)

i = 0


tmpList = [] #temporary list used in for-loop to keep track of current sequence
tempSeqCount = 1

longestSeq = [] #placeholder for final result
longestSeqCount = 0 

for nonPrime in nonPrimes:
    # compare current non-prime against previous non-prime
    # if previous == current - 1 then it is part of seq 
    if i > 0 and nonPrime - 1 == nonPrimes[i-1]:
        tmpList.append(nonPrime)
        tempSeqCount += 1 #increase seq counter
    else:
        # seq has endend, move temp list to placeholder if it's size is bigger than previous placeholder's size
        if tempSeqCount > longestSeqCount:
            longestSeq = tmpList
            longestSeqCount = tempSeqCount
        #create new tmp-list for next seq test and reset counter
        tmpList = [nonPrime]
        tempSeqCount = 1
    i += 1

print(f"The longest sequence non-primes under {highestPrime} starts at {longestSeq[0]} and ends at {longestSeq[longestSeqCount-1]}")
print(f"The sequence is {longestSeqCount} long.")
