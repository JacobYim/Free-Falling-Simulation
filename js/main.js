var particle_number = 250;
var window_width = 500;
var window_height = 500;
var density = particle_number/(window_width*window_height);

var T = 10000;
var k = 1;
var g = 10;
var dt = 0.01;
var t = 0.0;

var mp_m = 100;
var mp_r = 50;
var fp_m = mp_m/100;
var fp_r = mp_r/10;

var num_top = 0;
var num_bottom = 0;
var num_right = 0;
var num_left = 0;

function setup() {
  createCanvas(window_width, window_height);  
  mp = new main_particle(window_width, window_height, g, dt, mp_m, mp_r);
  fps = []
  for(var i = 0; i < particle_number; i++){
    fps[i] = new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, true, null);
  }
}

function draw() {
  background(220);
  
  // draw maim particle 
  ellipse(mp.x+window_width/2-mp.x, mp.y+window_height/2-mp.y, mp.r/2, mp.r/2);
  // draw free particles
  for (i = 0 ; i < fps.length ; i++){
      // update depend on whether collision occurred or not
      [collision_check, mp.vx, mp.vy, fps[i].x,fps[i].y, fps[i].vx, fps[i].vy] = calculate_particles_collision(fps[i], mp);
      // calculate next time steps of free particles
      fps[i].update();
      // update by the 
      if (check_remove_paricle(fps[i], mp, window_height, window_width)){
        fps.splice(i, 1);
      }else{
        ellipse(fps[i].x+window_width/2-mp.x, fps[i].y+window_height/2-mp.y, fps[i].r/2, fps[i].r/2);
      }
  }
  mp.update();
  // mp.vy = 5000;
  // add new particles
  [num_bottom, num_top, num_right, num_left] = calculate_paticles_to_add(mp, fp_m, fp_r, density, dt, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left);    
  console.log(round(t,4), mp.vy, mp.vx, density, fps.length/(window_width*window_height));
  t = t+dt;
}