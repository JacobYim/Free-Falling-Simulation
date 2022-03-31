import matplotlib.pyplot as plt
import csv
import os
import sys

times_list = []
vys_list = []
density_list = []

dir_name = sys.argv[1]
files = os.listdir(dir_name)

if sys.argv[2] == "MR" :
    files = list(filter( lambda x : float(x.split('_')[6])==float(sys.argv[3]), files))
elif sys.argv[2] == "T" :
    files = list(filter( lambda x : float(x.split('_')[4])==float(sys.argv[3]), files))
elif sys.argv[2] == "RR" :
    files = list(filter( lambda x : float(x.split('_')[5])==float(sys.argv[3]), files))

for file in files :
    with open(dir_name+'/'+file) as csvfile:
        times = []
        vys = []
        density = []
        spamreader = csv.reader(csvfile, delimiter=';')
        for i, row in enumerate(spamreader):
            if i > 0 and len(row) == 3:
                try :
                    temp_t, temp_vy, temp_density = list(map(lambda x : float(x), row))
                    times.append(temp_t)
                    vys.append(temp_vy)
                    density.append(temp_density)
                except :
                    print ("error", i, row)
        times_list.append(times)
        vys_list.append(vys)
        density_list.append(density)


for times, vys in zip(times_list, vys_list) :
    plt.plot(times, vys)
plt.savefig(sys.argv[2]+"_"+sys.argv[3]+"_tvsvy.jpg")

plt.clf()
plt.cla()

for times, density in zip(times_list, density_list) :
    plt.plot(times, density)
plt.savefig(sys.argv[2]+"_"+sys.argv[3]+"density.jpg")