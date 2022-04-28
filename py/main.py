from particle import MainParticle, FreeParticle, calculate_paticles_to_add
from multiprocessing import Process
from functions import calculate_particles_collision, check_remove_paricle, save
import os
import sys

particle_number = 250
window_width = 500
window_height = 500
T = 1000
k = 1
g = 10
dt = 0.01
procs_num = 100
radius_rate = 10
mass_rate = 100

def process(process_num, particle_number, window_width, window_height, T, k, g, dt, radius_rate, mass_rate, data_dir, reverse=False) :

    filename = "HIST_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(particle_number, window_width, window_height, T, radius_rate, mass_rate , k, g, dt)
    # length = len(list(filter(lambda x : filename in x,os.listdir(data_dir))))
    f = open(data_dir+'/'+filename+"_({})".format(process_num)+".csv", "a+")
    f.write("time;final_velocity;density\n")
    density = particle_number/(window_width*window_height)
    cnt_hit_cur_v = 0
    vys = []
    t = 0.0
    fp_m = 1
    fp_r = 1
    mp_r = fp_r*radius_rate
    mp_m = fp_m*mass_rate
    if reverse :
        mp_r = 10
        fp_r = 1*radius_rate

    num_top = 0
    num_bottom = 0
    num_right = 0
    num_left = 0

    mp = MainParticle(window_width, window_height, g, dt, mp_m, mp_r)
    fps = [FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, None, mp.vx, mp.vy) for _ in range(particle_number)]
    while (True) :
        for i in range(0, len(fps)) :
            # update depend on whether collision occurred or not
            [collision_check, mp.vx, mp.vy, fps[i].x,fps[i].y, fps[i].vx, fps[i].vy] = calculate_particles_collision(fps[i], mp)
            # calculate next time steps of free particles
            fps[i].update(mp)
            # update by the 
            if (check_remove_paricle(fps[i], mp, window_height, window_width)) :
                    fps[i] = None
        fps = list(filter(lambda x: x is not None, fps))   
        mp.update()
        # add new particles
        [fps, num_bottom, num_top, num_right, num_left] = calculate_paticles_to_add(mp, fps, fp_m, fp_r, density, dt, k, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left)           
        vwx = mp.vx
        vwy = mp.vy

        if (num_bottom > 0 ):
            for i in range(0, int(num_bottom)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "bottom", vwx, vwy))
            num_bottom = num_bottom - int(num_bottom)
            
        
        if (num_top > 0 ):
            for i in range(0, int(num_top)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "top", vwx, vwy))
            num_top = num_top - int(num_top)
            
        
        if (num_right > 0 ):
            for i in range(0, int(num_right)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "right", vwx, vwy))
            num_right = num_right - int(num_right)
            
        
        if (num_left > 0 ):
            for i in range(0, int(num_left)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "left", vwx, vwy))
            num_left = num_left - int(num_left)
        
        save(f, t, fps, mp, window_width, window_height)
        # print(t, round(mp.vy, 5), round(mp.vx, 5), density, len(fps)/(window_width*window_height))
        t = t+dt

        
        vys.append(mp.vy)
        if len(vys) > 1000 :
            if abs(sum(vys[-1000:])/1000 - mp.vy) < 0.1 :
                cnt_hit_cur_v += 1
            if cnt_hit_cur_v > 50 :
                break

    f.close()

if __name__ == '__main__':
    if sys.argv[1] == "RRR" :
        sim = {"sim_name":"RRR", "range": list(map(lambda x : x,  range( 1, 100)))} # fr/mr
    elif sys.argv[1] == "RR" :
        sim = {"sim_name":"RR", "range": list(map(lambda x : x,  range( 1, 100)))} # fr/mr
    elif sys.argv[1] == "MR" :
        sim = {"sim_name":"MR", "range": list(map(lambda x : x,  range( 1, 100)))} # fm/mm
    elif sys.argv[1] == "D" :
        sim = {"sim_name":"D",  "range": list(map(lambda x : x/1000, range( 1, 100)))}
    else :
        sim = {"sim_name":"T",  "range": list(map(lambda x : x*100,  range( 1, 100)))}
    print(sim['range'])
    data_dir = 'result_'+sim['sim_name']
    if not data_dir in os.listdir() :
        os.mkdir(data_dir)
    for num in range(int(procs_num)):
        if sim['sim_name'] == "T" :
            for T in sim['range'] :
                p =Process(target=process, args=(num, particle_number,                       window_width, window_height, T, k, g, dt, radius_rate, mass_rate, data_dir))
                p.start()
        elif sim['sim_name'] == "RR" :
            for rr in sim['range'] :
                p =Process(target=process, args=(num, particle_number,                       window_width, window_height, T, k, g, dt, rr, mass_rate, data_dir))
                p.start()
        elif sim['sim_name'] == "RRR" :
            for rr in sim['range'] :
                reverse=True
                p =Process(target=process, args=(num, particle_number,                       window_width, window_height, T, k, g, dt, rr, mass_rate, data_dir, reverse))
                p.start()
        elif sim['sim_name'] == "MR" :
            for mr in sim['range'] :
                p =Process(target=process, args=(num, particle_number,                       window_width, window_height, T, k, g, dt, radius_rate, mr, data_dir))
                p.start()
        elif sim['sim_name'] == "D" :
            for density in sim['range'] :
                p =Process(target=process, args=(num, int(density*window_height*window_width),    window_width, window_height, T, k, g, dt, radius_rate, mass_rate, data_dir))
                p.start()