import math
import random
from decimal import *
getcontext().prec = 1000


####    COMPRESSOR ####

# Set the probability distribution for all charachters
myProbs = [['0',Decimal(89)/Decimal(100)],
           ['1',Decimal(9)/Decimal(100)],
           ['.',Decimal(02)/Decimal(100)]]

# Build character probability dictionary
def makeProbs(myList):
	alphabet = ''
	chances = []
	for letter in myList:
		alphabet += letter[0]
		chances.append(letter[1])
	probs = {}
	for a in range(len(alphabet)):
		probs[alphabet[a]] = [Decimal(sum(chances[:a])), Decimal(sum(chances[:a+1]))]
	return probs

# Create a random string ('0','1')+ of length 'N'
# and rate of 'r' 1's, with '.' at the end
def makeString(N,r):
	xstring = ''
	for d in range(N):
		pick = random.random()
		dart = '1'
		if pick > r:
			dart = '0'
		xstring += dart
	return xstring + '.'

# Turn '00001000000000.' into [0.17812...,0.17815...]
def makeRawRange(myString,probs):
	a = Decimal(0)
	b = Decimal(1)
	totalsize = Decimal(1)
	for index in myString:
		size = b - a
		a += size*probs[index][0]
		b -= size*(Decimal(1)-probs[index][1])
	return [a,b]

# Turn [0.17812...,0.17815...] into [0.07861..., 0.07873...]
def makeBinRange(myRange):
	a = myRange[0]
	b = myRange[1]
	diff = b - a
	pwr = Decimal(0)
	while Decimal(2)**pwr > diff:
		pwr -= Decimal(1)
	interval = Decimal(2)**pwr
	timesx = Decimal(int(b/interval))
	inside = timesx*interval
	if inside + interval < b:# or b == 1:
		return [inside, (inside + interval)]
	elif inside - interval >= a:
		return [(inside-interval), inside]
	else:
		interval /= Decimal(2)
		if inside + interval < b:#	 or b == 1:
			return [inside, (inside + interval)]
		elif inside - interval >= a:
			return [(inside-interval), inside]

# Turn [0.07861..., 0.07873...] to '0001010000100'
def makeBinString(myList):
	myString = ''
	a = myList[0]
	b = myList[1]
	guess = Decimal(0)
	power = Decimal(-1)
	while guess != a:
		increment = Decimal(2)**power
		if a < guess + increment:
			myString += '0'
			power -= Decimal(1)
		else:
			myString += '1'
			power -= Decimal(1)
			guess += increment
	length = int((-1)*math.log(b-a,2))
	added = '0'*(length-len(myString))
	myString += added
	return myString

# The compressor
def compress(message,probs):
	letters = makeProbs(probs)
	rawRange = makeRawRange(message,letters)
	binRange = makeBinRange(rawRange)
	binString = makeBinString(binRange)
	return binString


#Execute Me!
message = makeString(50,.1)
compressed = compress(message,myProbs)
print 'COMPRESSOR'
print 'message    = ', message
print 'compressed = ', compressed





#####  DECOMPRESSOR  #####

# These first 20 lines are redundant, but they
# would be neccesary if the decompressor were 
# its own stand alone program.

import math
import random
from decimal import *
getcontext().prec = 1000

myProbs = [['0',Decimal(89)/Decimal(100)],
           ['1',Decimal(9)/Decimal(100)],
           ['.',Decimal(02)/Decimal(100)]]

# Build character probability dictionary
def makeProbs(myList):
	alphabet = ''
	chances = []
	for letter in myList:
		alphabet += letter[0]
		chances.append(letter[1])
	probs = {}
	for a in range(len(alphabet)):
		probs[alphabet[a]] = [Decimal(sum(chances[:a])),Decimal(sum(chances[:a+1]))]	
	return probs

# Turn 00111 into [0.21875,0.25]
def deMakeBinRange(myString):
	lower = Decimal(0)
	power = Decimal(-1)
	for ltr in myString:
		lower += Decimal(int(ltr)*Decimal(2)**power)
		power -= 1
	interval = Decimal(2)**(Decimal(-1)*Decimal(len(myString)))
	upper = lower + interval
	return [lower,upper]

# Turn [0.17812...,0.17815...] into '00001000000000.' 
def deMakeString(interval, letters):
	a = Decimal(interval[0])
	b = Decimal(interval[1])
	d = Decimal(0)
	u = Decimal(1)
	answer = ''
	while '.' not in answer:
		info = nextLetter(answer,a,b,d,u,letters)
		answer += info[0]
		d = info[1]
		u = info[2]
	return answer

# Append the next charachter in the message
def nextLetter(answer,a,b,d,u, letters):
	for z in letters:
		newd = (u-d)*letters[z][0] + d
		newu = (u-d)*letters[z][1] + d
		if newd <= a < b and (newu > b or newu == u):
			d = newd
			u = newu
			return [z,d,u]

# The decompressor
def deCompressor(myString, probs):
	letters = makeProbs(probs)
	deBinRange = deMakeBinRange(myString)
	answer = deMakeString(deBinRange,letters)
	return answer


# Execute me!
binString = compressed
answer = deCompressor(binString,myProbs)
print 'DECOMPRESSOR'
print 'compressed = ', binString
print 'message    = ', answer
print 'Comp. Rate = ', float(len(compressed))/len(message)