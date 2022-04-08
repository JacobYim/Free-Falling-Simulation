import csv
import matplotlib.pyplot as plt
filename = "result/1.csv"

def parse(filename):
    f = open(filename)
    csv_reader = csv.reader(f, delimiter=';')
    line_count = 0
    t_list = []
    mp_list = []
    fps_list = []
    for row in csv_reader:
        if line_count != 0:
            t_list.append(row[0])
            mp_list.append(row[1])
            fps_list.append(row[2])        
        line_count += 1
    return t_list, mp_list, fps_list

def calc_mp_ave_v(mp_vy_list):
    return sum(mp_vy_list[-500:])/500

# 종단속도 (온도, 시간)
def Average_Final_velocity_vs_Temperature(mp_vy_list_list, Ts):
    list_final_velocity = [calc_mp_ave_v(mp_vy_list) for mp_vy_list in mp_vy_list_list]
    plt.plot(list_final_velocity, Ts)

# 밀도 (온도, 시간)
def Average_Density_vs_Temperature(fp_list_list, Ts, width, hieght):
    list_density = [len(fp_list)/(width*hieght) for fp_list in fp_list_list]
    plt.plot(list_density, Ts)



        


# def plot_time_vs_density(list_t, list_fps) :
#     plt.plot(list_t,list(map(lambda x : len(x), list_fps)))
    
# def plot_time_vs_velocity(list_t, list_fps) :
#     plt.plot(list_t,list(map(lambda x : len(x), list_fps)))
    
# def plot_time_vs_density(list_t, list_fps) :
#     plt.plot(list_t,list(map(lambda x : len(x), list_fps)))
    
