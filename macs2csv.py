#Script for converting .dat files from the MACS public data set to .csv for
#use in R or whatever

#Usage:
#python <name>.dat <name>.inp

#Output:
#<name>.csv

#The input files need to be absolute. Output is written to ./

#To run on windows, file names delimiters will have to be changed

import sys
import csv

dat, inp = sys.argv[1:3]
csv_name = dat.strip().split('/')[-1].split('.')[0]
csv_name = csv_name + ".csv"

csvWtr = csv.writer(open(csv_name, 'wb'), delimiter=',', quotechar='|',
quoting=csv.QUOTE_MINIMAL)

#process the SAS input file
tmp = open(inp)
inp_l = [x.strip() for x in tmp]
tmp.close()

vnames, ends = [], []
for i, l in enumerate(inp_l):
	if l.startswith('/*') or l.startswith('INPUT') or l.startswith(';'):
		pass
	else:
		#colums are seperated by some number of " "
		splt = l.split(' ')
		vnames.append(str(splt[0]))
		rng = splt[-1]
		tok = rng.split('-')
		if len(tok) is 1:
			tok = filter(lambda x: x.isdigit(), tok[0])
			ends.append(int(tok))
		elif len(tok) is 2:
			tok = filter(lambda x: x.isdigit(), tok[1])
			ends.append(int(tok))
		else:
			print "Weird number formating in line", i

#process the .dat file
tmp = open(dat)
dat_l = [x.strip() for x in tmp]
tmp.close()

dat = []
for l in dat_l:
	tokens = []
	start, end = 0, 0
	for new_end in ends:
		end = new_end
		token = l[start:end]
		token = filter(lambda x: x.isdigit(), token)
		if len(token) is 0:
			token = " "
		tokens.append(token)
		start = end
	dat.append(tokens)

csvWtr.writerow(vnames)
for d in dat:
	csvWtr.writerow(d)




