import pandas as pd
import os
import math


global Dref1
global Dref2
global Dref3
global Dref4
dref1 = 2.6451
dref2 = 2.5455
dref3 = 0.9508
dref4 = 0.4625

def main():
	df=pd.read_excel("measurements.xlsx",engine='openpyxl',index_col=None, header=None)
	event = []
	for column in df:
		#print(df[column][1])
		#get the caculated values
		#print()
		dfr = formula(df[column][0],df[column][1],df[column][8])
		dto = formula(df[column][2],df[column][3],df[column][9])
		dinj1 = formula(df[column][4],df[column][5],df[column][8])
		dinj2 = formula(df[column][6],df[column][7],df[column][9])

		d1 = abs(dfr-dref1)
		d2 = abs(dto-dref2)
		d3 = abs(dinj1-dref3)
		d4 = abs(dinj2-dref4)

		d = d1+d2+d3+d4
		# print(dfr)
		# print(dto)
		# print(dinj1)
		# print(dinj2)
		#print(d)
		
		#1 means attacked, 0 means normal
		if d>0.15:
			event.append(1)
		else:
			event.append(0)

	print(event)


def formula(n1,n2,d1):
	result = math.sqrt(n1**2+n2**2)/(d1**2)

	return result


if __name__ == "__main__":
	main()
