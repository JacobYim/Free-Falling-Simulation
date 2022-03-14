import math
import random
from functions import Finv, F, erfc

class MainParticle :
    def __init__ (self, width, height, g, dt, mass, r) :
        self.r = r
        self.width = width
        self.height = height
        self.mass = mass
        self.g = g
        self.dt = dt
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0

    def update(self) :
        self.vy = self.vy + self.g * self.dt
        self.x  = self.x + self.vx * self.dt
        self.y  = self.y + self.vy * self.dt
    
class FreeParticle :
    def __init__ (self, width, height, g, dt, mass, r, T, k, mp, position, vwx, vwy) :
        self.r = r
        self.width = width
        self.height = height
        self.mass = mass
        self.g = g
        self.dt = dt
        self.T = T
        self.k = k

        alpha = math.sqrt(self.mass/(2*self.k*self.T))

        rand_num1 = round(random.random(),4)
        rand_num2 = round(random.random(),4)
        
        vx1 = Finv(F, alpha, vwx, rand_num1)*(-1)
        vx2 = Finv(F, alpha, vwx*(-1), rand_num1)
        vy1 = Finv(F, alpha, vwy, rand_num2)*(-1)
        vy2 = Finv(F, alpha, vwy*(-1), rand_num2)

        if position == 'left' :
            self.y = random.randrange((-1)*self.height/2, self.height/2)+mp.y
            self.x = -self.width/2+mp.x
            if (random.choice([-1, 1]) == -1):
                self.vy = vy1
            else :
                self.vy = vy2
            self.vx = vx2
            # radian=random.randrange(270,450)*(2*math.pi/360)
            # radian=random.randrange(315,405)*(2*math.pi/360)
            # radian=360*(2*math.pi/360)

        elif position == 'right' :
            self.y = random.randrange((-1)*self.height/2, self.height/2)+mp.y
            self.x = self.width/2+mp.x
            if (random.choice([-1, 1]) == -1) :
                self.vy = vy1
            else :
                self.vy = vy2
            
            self.vx = vx1
            # radian=random.randrange(90,270)*(2*math.pi/360)
            # radian=random.randrange(135,225)*(2*math.pi/360)
            # radian=180*(2*math.pi/360)
        elif position == 'top' :
            self.x = random.randrange((-1)*self.width/2, self.width/2)+mp.x
            self.y = -self.height/2+mp.y
            if (random.choice([-1, 1]) == -1):
                self.vx = vx1
            else:
                self.vx = vx2
            self.vy = vy2
            # self.vx = vx*random.choice([-1, 1])
            radian=random.randrange(0,180)*(2*math.pi/360)
            # radian=random.randrange(45,135)*(2*math.pi/360)
            # radian=90*(2*math.pi/360)
        elif position == 'bottom' :
            self.x = random.randrange((-1)*self.width/2, self.width/2)+mp.x
            self.y = self.height/2+mp.y
            if (random.choice([-1, 1]) == -1):
                self.vx = vx1
            else:
                self.vx = vx2
            
            self.vy = vy1
            radian=random.randrange(180,360)*(2*math.pi/360)
            # radian=random.randrange(225,315)*(2*math.pi/360)
            # radian=270*(2*math.pi/360)

        else :
            if position == None :
                dx = 0.0
                dy = 0.0
                dist = mp.r/2+self.r/2
                while(dx*dx+dy*dy < dist*dist):
                    self.x = random.randrange((-1)*self.width/2, self.width/2)
                    self.y = random.randrange((-1)*self.height/2, self.height/2)
                    dx = self.x-mp.x
                    dy = self.y-mp.y
                
                self.vx = random.choice([-1, 1]) * random.gauss(0, math.sqrt(self.k*self.T/(self.mass)))
                self.vy = random.choice([-1, 1]) * random.gauss(0, math.sqrt(self.k*self.T/(self.mass)))
                # radian = random.randrange(0,360)*(2*math.pi/360)
            else :
                raise Exception("Invalid initializing position")
        
        # var v = math.sqrt(this.vx**2+this.vy**2)
        # this.vx = v*cos(radian)
        # this.vy = v*sin(radian)

    def update(self, mp) :
        self.x = self.x + (self.vx ) * self.dt
        self.y = self.y + (self.vy ) * self.dt

def calculate_paticles_to_add(mp, fps, fp_m, fp_r, density, dt, k, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left):
    # k = 1
    a = math.sqrt(2*k*T/fp_m)
    vwx = mp.vx      # - : windonw move left (particle right), + : windonw move right (particle left)
    vwy = mp.vy      # + : windonw move top (particle bottom), - : windonw move bottom (particle top)

    num_right   += density * math.sqrt((2*k*T)/(fp_m)) * dt / 2 * (math.exp(-1*(vwx/a)**2)/math.sqrt(math.pi) +(vwx/a)*erfc((-1)*vwx/a)) * window_height
    num_left    += density * math.sqrt((2*k*T)/(fp_m)) * dt / 2 * (math.exp(-1*(vwx/a)**2)/math.sqrt(math.pi) -(vwx/a)*erfc(vwx/a)) * window_height
    num_bottom  += density * math.sqrt((2*k*T)/(fp_m)) * dt / 2 * (math.exp(-1*(vwy/a)**2)/math.sqrt(math.pi) +(vwy/a)*erfc((-1)*vwy/a)) * window_width
    num_top     += density * math.sqrt((2*k*T)/(fp_m)) * dt / 2 * (math.exp(-1*(vwy/a)**2)/math.sqrt(math.pi) -(vwy/a)*erfc(vwy/a)) * window_width
    
    return [fps, num_bottom, num_top, num_right, num_left]
