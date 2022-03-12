var particle_number = 250;
var window_width = 500;
var window_height = 500;
var density = particle_number/(window_width*window_height);

var T = 1000;
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

// initial setting for printing result
// let result_list = [
//   'T : '+String(T)+' g : '+String(g)+' particle_number : '+ String(particle_number) + ' window_width : '+String(window_width) +' window_height : '+String(window_height) +' density : '+String(density),
//   'Time;main_x;main_y;main_vx;main_vy;free_vx_list;free_vy_list'
// ];
// function mousePressed() {
//   if (mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height) {
//     saveStrings(result_list, 'infinity_silindar.txt');
//   }
// }

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
        fps[i].update(mp);
        // update by the 
        if (check_remove_paricle(fps[i], mp, window_height, window_width)){
            // if (fp_coord_x < fps[i].r || fp_coord_x > window_width-fps[i].r){
            //   fps[i].vx = (-1)* fps[i].vx;
            // }else{
                fps.splice(i, 1);
            // }
        }else{
            ellipse(fps[i].x+window_width/2-mp.x, fps[i].y+window_height/2-mp.y, fps[i].r/2, fps[i].r/2);
        }
    }
    mp.update();
    // add new particles
    [num_bottom, num_top, num_right, num_left] = calculate_paticles_to_add(mp, fp_m, fp_r, density, dt, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left);    
    console.log(mp.vy, num_top, num_bottom, density, fps.length/(window_width*window_height));
    t = t+dt;
  
//   var fpvx_list = [];
//   var fpvy_list = [];
//   for (i = 0 ; i < fps.length ; i++){
//     fpvx_list.push(fps[i].vx);
//     fpvy_list.push(fps[i].vy);
//   }
//   result_list.push(String(t)+';'+String(mp.x)+';'+String(mp.y)+';'+String(mp.vx)+';'+String(mp.vy)+';'+fpvx_list.toString()+';'+fpvy_list.toString());
}