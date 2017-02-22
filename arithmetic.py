import math
import random
from decimal import *
getcontext().prec = 1000


####    COMPRESSOR    ####

# Build character probability dictionary
def makeSpectrum(myDict):
	total = sum(myDict.values())
	while True:
		for char in myDict:
			adjusted = round(myDict[char]/total,5)
			myDict[char] = Decimal("{:.5f}".format(adjusted))
		total = sum(myDict.values())
		if total <= 1:
			break
		total *= Decimal(1001)/Decimal(1000)
	alphabet = ''
	chances = []
	for letter in myDict:
		alphabet += letter
		chances.append(myDict[letter])
	probs = {}
	for a in range(len(alphabet)):
		probs[alphabet[a]] = [sum(chances[:a]), sum(chances[:a+1])]
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
	a = 0
	b = 1
	totalsize = 1
	for index in myString:
		size = b - a
		a += size*probs[index][0]
		b -= size*(1-probs[index][1])
	return [a,b]

# Turn [0.17812...,0.17815...] into [0.07861..., 0.07873...]
def makeBinRange(myRange):
	a = myRange[0]
	b = myRange[1]
	diff = b - a
	pwr = 0
	while 2**pwr > diff:
		pwr -= 1
	interval = Decimal(2)**pwr
	timesx = int(b/interval)
	inside = timesx*interval
	if inside + interval < b or (inside + interval == b ==1):
		return [inside, (inside + interval)]
	elif inside - interval >= a:
		return [(inside-interval), inside]
	else:
		interval /= 2
		if inside + interval < b or (inside + interval == b ==1):
			return [inside, (inside + interval)]
		elif inside - interval >= a:
			return [(inside-interval), inside]

# Turn [0.07861..., 0.07873...] to '0001010000100'
def makeBinString(myList):
	myString = ''
	a = myList[0]
	b = myList[1]
	guess = 0
	power = -1
	while guess != a:
		increment = Decimal(2)**power
		if a < guess + increment:
			myString += '0'
			power -= 1
		else:
			myString += '1'
			power -= 1
			guess += increment
	length = int((-1)*math.log(b-a,2))
	added = '0'*(length-len(myString))
	myString += added
	return myString

# The compressor
def compress(message,spectrum):
	rawRange = makeRawRange(message,spectrum)
	binRange = makeBinRange(rawRange)
	binString = makeBinString(binRange)
	return binString






#####  DECOMPRESSOR  #####

# Turn 00111 into [0.21875,0.25]
def deMakeBinRange(myString):
	lower = 0
	power = -1
	for ltr in myString:
		lower += int(ltr)*Decimal(2)**power
		power -= 1
	interval = 2**(Decimal(-1)*len(myString))
	upper = lower + interval
	return [lower,upper]

# Turn [0.17812...,0.17815...] into '00001000000000.' 
def deMakeString(interval, letters):
	a = interval[0]
	b = interval[1]
	d = 0
	u = 1
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
def deCompressor(myString, spectrum):
	deBinRange = deMakeBinRange(myString)
	answer = deMakeString(deBinRange,spectrum)
	return answer




####   EXECUTE ME!   ####


# Set Probabilities. If the compressor and decompressor
# were in two separate files, each one would need
# these probabilities, the 'makeSpectrum' function,
# and the decimal and math libraries.

myProbs = { '0': Decimal(89),
			'1': Decimal(10),
			'.': Decimal(1)}

spectrum =  makeSpectrum(myProbs)

print "PROBS:"
for a in myProbs:
	print a, ':', myProbs[a]


# Compress
message = makeString(60,0.1)
compressed = compress(message,spectrum)
print '\nCOMPRESSOR:'
print '\nmessage    = ', message
print 'compressed = ', compressed

# Decompress
binString = compressed
answer = deCompressor(binString,spectrum)
print '\nDECOMPRESSOR:'
print '\ncompressed = ', binString
print 'message    = ', answer
print '\nmatch? ', message==answer
print '\ncomp. Rate = ', float(len(compressed))/len(message), '\n'


# Average over 10 tries
for size in [100,200,400,800]:
  	meanList = []
  	for index in range(10):
  		myMessage = makeString(size,0.1)
  	 	myCompress = compress(myMessage,spectrum)
  	 	meanList += [float(len(myCompress))/len(myMessage)]
  	print 'Average Rate,', size, 'chars =', round(sum(meanList)/len(meanList),4)




####   THREORY  ####

# Shannon Information Content
def sic(x):
	return math.log(1/x,2)

# Entropy
def H(x):
	sum = 0
	if type(x) is list:
		for a in x:
			a = float(a)
			sum += a*sic(a)
	elif type(x) is float:
		sum = x*math.log(1/x,2) + (1-x)*math.log(1/(1-x),2)
	else:
		print 'please enter a list or float'
	return sum

# Theoretical limit
print 'Theoretical Limit       =', round(H([0.1,0.9]),4)





