import matplotlib.pyplot as plt
import csv
import os

times_list = []
vys_list = []
density_list = []

dir_name = "test_result_MR"
files = os.listdir(dir_name)
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
            else :
                print (i, row)
        times_list.append(times)
        vys_list.append(vys)
        density_list.append(density)


for times, vys in zip(times_list, vys_list) :
    plt.plot(times, vys)
plt.savefig("tvsvy.jpg")

plt.clf()
plt.cla()

for times, density in zip(times_list, density_list) :
    plt.plot(times, density)
plt.savefig("density.jpg")