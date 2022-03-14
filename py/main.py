from particle import MainParticle, FreeParticle, calculate_paticles_to_add
from functions import calculate_particles_collision, check_remove_paricle, save
from multiprocessing import Process
from tqdm import tqdm
import os

particle_number = 250
window_width = 500
window_height = 500
T = 1000
k = 1
g = 10
dt = 0.01
procs_num = 100
def process(particle_number, window_width, window_height, T, k, g, dt) :

    filename = "HIST_{}_{}_{}_{}_{}_{}_{}".format(particle_number, window_width, window_height, T, k, g, dt)
    length = len(list(filter(lambda x : filename in x,os.listdir())))
    f = open(filename+"_({})".format(length)+".csv", "a+")
    f.write("time;mp;list_fps\n")

    density = particle_number/(window_width*window_height)
    t = 0.0
    mp_m = 100
    mp_r = 50
    fp_m = mp_m/100
    fp_r = mp_r/10

    num_top = 0
    num_bottom = 0
    num_right = 0
    num_left = 0

    mp = MainParticle(window_width, window_height, g, dt, mp_m, mp_r)
    fps = [FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, None, mp.vx, mp.vy) for _ in tqdm(range(particle_number), ascii=True ,desc="generationg free particles ...".format(t))]

    while (True) :
        for i in tqdm(range(0, len(fps)), ascii=True ,desc="{}".format(round(t,3))) :
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
                num_bottom = num_bottom - 1
            
        
        if (num_top > 0 ):
            for i in range(0, int(num_top)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "top", vwx, vwy))
                num_top = num_top - 1
            
        
        if (num_right > 0 ):
            for i in range(0, int(num_right)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "right", vwx, vwy))
                num_right = num_right - 1
            
        
        if (num_left > 0 ):
            for i in range(0, int(num_left)):
                fps.append(FreeParticle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "left", vwx, vwy))
                num_left = num_left - 1
        
        save(f, t, fps, mp)
        # print(t, round(mp.vy, 5), round(mp.vx, 5), density, len(fps)/(window_width*window_height))
        t = t+dt

if __name__ == '__main__':
    for num in range(procs_num):
        p =Process(target=process, args=(particle_number, window_width, window_height, T, k, g, dt))
        p.start()