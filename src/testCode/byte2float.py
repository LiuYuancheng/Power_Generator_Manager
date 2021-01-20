def ieee745ToDec(N): # ieee-745 bits (max 32 bit)
	N = N.replace("0x",'')
	
	N = bin(int(N, 16)).replace('0b','')
	N = N.zfill(32)
	#print(N)
	a = int(N[0])        # sign,     1 bit
	b = int(N[1:9],2)    # exponent, 8 bits
	c = int("1"+N[9:], 2)# fraction, len(N)-9 bits


	decimal = (-1)**a * c /( 1<<( len(N)-9 - (b-127) ))
	binary = N
	return decimal

#print(ieee745ToDec('01000000010010010000111111111001'))  # -->  3.1416
					  #1000000010010010000111111111001
#print(ieee745ToDec('10111111101000000000000000000000')) # --> -1.25

print(ieee745ToDec('0x40490FF9'))  # -->  3.1416
print(ieee745ToDec('0xBFA00000')) # --> -1.25