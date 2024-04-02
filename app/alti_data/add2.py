import numpy as np

with open('list.txt', 'r') as lis:
    list_file_name = []
    for fileN in lis:
        list_file_name.append(fileN[:-1])

for fileN in list_file_name:
    tile = np.array((int(fileN[30:34]), int(fileN[35:39])))
    req1 = tile - np.array((0, 1))
    req2 = tile + np.array((1, 0))
    req3 = tile + np.array((1, -1))

    #print(tile, req1, req2, req3)
    req1_name = f"SWISSALTI3D_2_XYZ_CHLV95_LN02_{str(req1[0])}_{str(req1[1])}.xyz"
    req2_name = f"SWISSALTI3D_2_XYZ_CHLV95_LN02_{str(req2[0])}_{str(req2[1])}.xyz"
    req3_name = f"SWISSALTI3D_2_XYZ_CHLV95_LN02_{str(req3[0])}_{str(req3[1])}.xyz"
    on = True

    if not req1_name in list_file_name or not req2_name in list_file_name or not req3_name in list_file_name:
        continue

    with open(f"ld/{fileN}", 'r') as inn:
        with open(f"trans2/{fileN}", 'w') as edited:
            for line in inn:
                edited.write(line)

    with open(f"trans2/{fileN}", 'a+') as edited:
        with open(f"ld/{req1_name}", 'r') as file1:
            y_search = tile[1]*1000-1
            #print(y_search)
            for line in file1:
                if int(line[8:15]) == y_search:
                    if on:
                        edited.write(line[:-1])
                        on = False
                    else:
                        edited.write('\n' + line[:-1])
        
        line_ad = []

        with open(f"ld/{req2_name}", 'r') as file2:
            x_search = (tile[0]+1)*1000+1
            #print(x_search)
            for line in file2:
                if int(line[0:7]) == x_search:
                    line_ad.append(line)
                    #print(line[:-1])

        with open(f"ld/{req3_name}", 'r') as file3:
            line_end = file3.readline()
            

    i = 0

    with open(f"trans2/{fileN}", 'r') as file:
        with open(f"ld3/{fileN}", 'w') as edited2:
            for line in file:
                if line[4:7] == "901":
                    edited2.write(line)
                    try:
                        edited2.write(line_ad[i])
                        i+=1
                    except:
                        edited2.write('\n' + line_end[:-1])
                else:
                    edited2.write(line)
            


        
'''inFile = open(fileN, 'w+')
        outFile = open(f'./parthed/{file}', 'w')

        n = 500#ld = 500 hd = 
        saute = 50#ld = 50 hd = 

        inFile.readline()
        for i, line in enumerate(inFile):
            if i%saute == 0:
                if (i//500)%saute == 0:
                    outFile.write(line)

        inFile.close()
        outFile.close()'''

#swissalti3d_2021_2576-1164_2_2056_5728.xyz
#SWISSALTI3D_2_XYZ_CHLV95_LN02_2576_1164.xyz
#file = dos[0:11].upper() + "_2_XYZ_CHLV95_LN02_" + dos[17:26].replace("-", "_") + ".xyz"