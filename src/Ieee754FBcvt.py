#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        Ieee754FBcvt.py
#
# Purpose:     This module is used to convert bytes string to float number or 
#              reverse the calculation based on the Ieee754 stand.
# Author:      Yuancheng Liu
#
# Created:     2021/01/27
# Copyright:   N.A (editted by YC)
# License:     N.A (editted by YC)
#--------------------------------------------------------------------------

def B2F(bytesStr):  # ieee-745 bits (max 32 bit)
    """ Byte String to float number.
    Args:
        N ([String]): [description]
    Returns:
        [fload]: [description]
    """
    N = bin(int(bytesStr.replace("0x", ''), 16)).replace('0b', '')
    N = N.zfill(32)
    sign = int(N[0])                # sign,     1 bit
    exponent = int(N[1:9], 2)       # exponent, 8 bits
    fraction = int("1"+N[9:], 2)    # fraction, len(N)-9 bits
    return (-1)**sign * fraction / (1 << (len(N)-9 - (exponent-127)))

#--------------------------------------------------------------------------
def floatBin(num, places = 4):
    whole, dec = str(num).split(".")
    res = (str(bin(int(whole)))+".").replace('0b','')
    for _ in range(places):
        dec = str('0.')+str(dec)
        temp = '%1.20f' %(float(dec)*2)
        whole, dec = temp.split(".")
        res += whole
    return res

#--------------------------------------------------------------------------
def F2B(num, places = 30):
    # identifying whether the number
    # is positive or negative
    sign = 0 if num > 0 else 1
    num = abs(num)

    # convert float to binary
    dec = floatBin(num, places = places)

    # finding the mantissa
    dotIdx, oneIdx= dec.find('.'), dec.find('1')
    dec = dec.replace(".","")
    dotIdx -= 1
    if oneIdx > dotIdx: oneIdx -= 1
    mantissa = dec[oneIdx+1:]
    # calculating the exponent(E)
    exponentBits = dotIdx - oneIdx + 127
    # converting the exponent from
    # decimal to binary
    exponentBits = bin(exponentBits).replace("0b",'')
    mantissa = mantissa[0:23]

    # the IEEE754 notation in binary    
    final = str(sign) + exponentBits.zfill(8) + mantissa

    # convert the binary to hexadecimal
    return '0x%0*X' %((len(final) + 3) // 4, int(final, 2))
    #return (hstr, final)

#--------------------------------------------------------------------------

print(B2F('0x40490FF9'))  # -->  3.1416
print(B2F('0xBFA00000'))  # --> -1.25

print(F2B(3.1415998935699463))
print(F2B(-1.25))
