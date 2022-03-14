import math
import numpy as np

def save(f, t, fps, mp, width, height):
    # text = "{};{};{}\n".format(t, {"x": mp.x, "y": mp.y, "vx": mp.vx, "vy":mp.vy}, list(map(lambda fp : {"x": fp.x, "y": fp.y, "vy":fp.vy, "vx":fp.vx}, fps)))
    text = "{};{};{}\n".format(t, mp.vy, len(fps)/(width*height))
    f.write(text)

def erf(x):
    return math.erf(x)
    # retval = 0.0
    # neg = False
    # if (x < 0):
    #   neg = True
    #   x = (-1)*x
     
    # dx = x/1000
    
    # if (x == 0.0) :
    #     x = 1e-15

    # # for i in list(np.arange(0, x, x/1000)) :
    # #   retval += dx * math.exp(-1*(i**2))
    
    # retval = sum([math.exp(-1*(i**2)) for i in list(np.arange(0, x, x/1000))])*dx

    # retval = retval*2/math.sqrt(math.pi)
    # if (retval > 1):
    #   retval = 1.0
    
    # if(abs(retval) == 0) :
    #     retval = 1e-15
    # else :
    #     retval = retval

    # if (neg):
    #   retval = (-1)*retval
        
    # return retval


def A (alpha, vw, x) :
    return 1/(2*alpha*math.sqrt(math.pi))*(-math.exp(-1*(alpha*(vw+x))**2))

def B (alpha, vw, x) :
    return 1/2*(erf(alpha*(vw+x))-1)

def f(alpha, vw, x) :
# console.log("in f",x, A(alpha, vw, x), B(alpha, vw, x))
    return A(alpha, vw, x) - vw * B(alpha, vw, x)

def F(alpha, vw, x) :
# console.log("in F", x, f(alpha,vw, x), f(alpha, vw, 0))
    retval = f(alpha, vw, 0)
    if retval == 0 :
        retval = 1e-15
    return 1-(f(alpha,vw,x)/retval)

def Finv(F, alpha, vw, y):
    x = 0
    dx = 1
    transition = [False, False]
    error = y - F(alpha, vw, x)
    # console.log("F(alpha, vw, x)", F(alpha, vw, x))
    # console.log("error", error)
    while (abs(error) > 1e-9) :
        # console.log(x, "error", error)
        if (error > 0) :
            # print("error > 0")
            transition[0] = True
            x = x + dx
            # print("y", y,"x", x, "alpha", alpha)
            # print("check", error, y - F(alpha, vw, x))
            # print("check", y - F(alpha, vw, 0), y - F(alpha, vw, 1), y - F(alpha, vw, 2), y - F(alpha, vw, 300000))
            # print(F(alpha, vw, 0), F(alpha, vw, 1), F(alpha, vw, 2), F(alpha, vw, 300000))
        
        if (error < 0) :
            # print("error < 0")
            transition[1] = True
            x = x - dx
            # print("x", x)
            # print("check", error, y - F(alpha, vw, x))
            # print("check", y - F(alpha, vw, 0), y - F(alpha, vw, 1), y - F(alpha, vw, 2), y - F(alpha, vw, 3))
        
        if (transition[0] and transition[1]) :
            dx = dx * 0.1
            transition = [False, False]
        
        if (error == y - F(alpha, vw, x)) :
            break
        
        error = y - F(alpha, vw, x)
    
    return x

def erfc(x) :
    return 1-erf(x)

def collision2d(ma, mb, vax, vbx, vay, vby, sin, cos):
    e = 1
    vaxp = (ma-e*mb)/(ma+mb)*(vax*cos+vay*sin)+(mb+e*mb)/(ma+mb)*(vbx*cos+vby*sin)
    vbxp = (ma+e*ma)/(ma+mb)*(vax*cos+vay*sin)+(mb-e*ma)/(ma+mb)*(vbx*cos+vby*sin)
    vayp = vay*cos - vax*sin
    vbyp = vby*cos - vbx*sin
    
    vaxp2 = vaxp*cos-vayp*sin
    vayp2 = vaxp*sin+vayp*cos
    vbxp2 = vbxp*cos-vbyp*sin
    vbyp2 = vbxp*sin+vbyp*cos
    
    return [vaxp2, vbxp2, vayp2, vbyp2]

def calculate_particles_collision(fp, mp):

    collision_check = False
    new_fp_x = fp.x
    new_fp_y = fp.y
    new_fp_vx = fp.vx
    new_fp_vy = fp.vy
    new_mp_vx = mp.vx
    new_mp_vy = mp.vy
    
    dx = fp.x-mp.x
    dy = fp.y-mp.y
    if (dx*dx+dy*dy < mp.r/2*mp.r/2):
        collision_check = True
        col_angle_sin = dy/math.sqrt(dx*dx+dy*dy)
        col_angle_cos = dx/math.sqrt(dx*dx+dy*dy)
        list_v = collision2d(mp.mass, fp.mass, mp.vx, fp.vx, mp.vy, fp.vy, col_angle_sin, col_angle_cos)
        new_mp_vx = list_v[0]
        new_fp_vx = list_v[1]
        new_mp_vy = list_v[2]
        new_fp_vy = list_v[3]      
        new_fp_y = mp.y  + col_angle_sin*(mp.r/2)
        new_fp_x = mp.x  + col_angle_cos*(mp.r/2)

    return [collision_check,new_mp_vx,new_mp_vy,new_fp_x,new_fp_y,new_fp_vx,new_fp_vy]

def check_remove_paricle(fp, mp, window_height, window_width):
    # calculate coodinate
    fp_coord_x = fp.x+window_width/2-mp.x
    fp_coord_y = fp.y+window_height/2-mp.y
    
    # remove the out of window
    if (fp_coord_x < 0 or fp_coord_x > window_width or fp_coord_y < 0 or fp_coord_y > window_height):
        return True
    else:
        return False
    
