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


def float_bin(my_number, places = 4):
    my_whole, my_dec = str(my_number).split(".")
    my_whole = int(my_whole)
    res = (str(bin(my_whole))+".").replace('0b','')
 
    for x in range(places):
        my_dec = str('0.')+str(my_dec)
        temp = '%1.20f' %(float(my_dec)*2)
        my_whole, my_dec = temp.split(".")
        res += my_whole
    return res
 
 
 
def IEEE754(n) :
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0 :
        sign = 1
        n = n * (-1)
    p = 30
    # convert float to binary
    dec = float_bin (n, places = p)
 
    dotPlace = dec.find('.')
    onePlace = dec.find('1')
    # finding the mantissa
    if onePlace > dotPlace:
        dec = dec.replace(".","")
        onePlace -= 1
        dotPlace -= 1
    elif onePlace < dotPlace:
        dec = dec.replace(".","")
        dotPlace -= 1
    mantissa = dec[onePlace+1:]
 
    # calculating the exponent(E)
    exponent = dotPlace - onePlace
    exponent_bits = exponent + 127
 
    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).replace("0b",'')
 
    mantissa = mantissa[0:23]
 
    # the IEEE754 notation in binary    
    final = str(sign) + exponent_bits.zfill(8) + mantissa
 
    # convert the binary to hexadecimal
    hstr = '0x%0*X' %((len(final) + 3) // 4, int(final, 2))
    return (hstr, final)
 
# Driver Code
if __name__ == "__main__" :
    print (IEEE754(3.1416))
    print (IEEE754(-1.25))