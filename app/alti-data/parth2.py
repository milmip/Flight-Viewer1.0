

with open('list.txt', 'r') as lis:
	for dos in lis:
		file = dos[0:11].upper() + "_2_XYZ_CHLV95_LN02_" + dos[17:26].replace("-", "_") + ".xyz"
		inFile = open(f'./unzip/{dos[:-1]}/{file}', 'r')
		outFile = open(f'./firstlayer/ld/{file}', 'w')

		n = 500#ld = 500 hd = 
		saute = 50#ld = 50 hd = 

		inFile.readline()
		for i, line in enumerate(inFile):
			if i%saute == 0:
				if (i//500)%saute == 0:
					outFile.write(line)

		inFile.close()
		outFile.close()

#swissalti3d_2021_2576-1164_2_2056_5728.xyz
#SWISSALTI3D_2_XYZ_CHLV95_LN02_2576_1164.xyz