import operator as op
import random
import math
random.seed()

#Shannon Information Content
def h(x):
	return math.log(1/x,2)

#Entropy
def H(x):
	sum = 0
	if type(x) is list:
		for a in x:
			sum += a*h(a)
	elif type(x) is float:
		sum = x*math.log(1/x,2) + (1-x)*math.log(1/(1-x),2)
	else:
		print 'please enter a list or float'
	return sum




####   COMPRESSOR  ####
# This is a symbolic compressor. It takes 8 or more bits at a time and
# (usually) turns them into a shorter sequence.
# The average compression rate is 0.53

# 101 -> 5
def unBinary(y):
	sum = 0
	y = y[::-1]
	for a in range(len(y)):
		if y[a]=='1':
			sum += 2**a
	return sum

#Turns 2 -> '010' for 8-bit compression, -> '0010' for 16 bit
def binaryFull(index,bit):
	binaryIndex = int(bin(index)[2:])
	lenIndex = len(str(binaryIndex))
	ohs =  '0'*(int(math.log(bit,2) - lenIndex))
	full = ohs + str(binaryIndex)
	return full

#Creates short string at code's head to indicate how many bits short of a bit*n the input is
def prefix(string, bit):
	short = binaryFull((len(string)*(-1))%bit,bit)
	return str(short)

#creates random string of length 'N' and rate of ones 'r'
def makeString(N,r):
	xstring = ''
	for d in range(N):
		pick = random.random()
		if pick > r:
			dart = 0
		else:
			dart = 1
		xstring += str(dart)
	return xstring

#How a x-bit string is compressed in the compressor
def code(string,bit):
	c = ''
	ones = string.count('1')
	if ones == 0:
		c = '0'
	else:
		for index in range(len(string)):
			if string[index] == '1':
				c += '1' + binaryFull(index,bit)
		c += '0'
	return c

#The compressor. Begins with prefix, runs code(string,bit) repeatedly.
def compressor(string, bit):
	shortString = prefix(string, bit)
	string += unBinary(shortString)*'0'
	while string:
		part = string[:bit]
		string = string[bit:]
		add = code(part,bit)
		shortString += add		
	return shortString


# Execute Me!
print 'COMPRESSOR'

message = makeString(60,0.1)
print 'message = ', message
compressed = compressor(message,8)
print 'message    = ', message
print 'compressed = ', compressed








####    DECOMPRESSOR   ####

def unBinary(y):
	sum = 0
	y = y[::-1]
	for a in range(len(y)):
		if y[a]=='1':
			sum += 2**a
	return sum

def decompress(string, bit):
	longString = ''
	prefix = string[:int(math.log(bit,2))]
	string = string[int(math.log(bit,2)):]
	while string:
		numbers = []
		signal = string[0]
		part = '0'*bit
		while signal == '1':
			string = string[1:]
			numbers.append(unBinary(string[:int(math.log(bit,2))]))
			string = string[int(math.log(bit,2)):]
			signal = string[0]
		if signal == '0':
			signal = string[0]
			string = string[1:]
		for a in numbers:
			part = part[:a] + '1' + part[(a + 1):]
		longString += part
	numPrefix = unBinary(prefix)
	if numPrefix:
		longString = longString[:-numPrefix]
	return longString




# Execute me!
print "DECOMPRESSOR"
print 'compressed = ', compressed	
print 'message    = ', decompress(compressed, 8)
print "comp. rate = ", len(compressed)/float(len(message))