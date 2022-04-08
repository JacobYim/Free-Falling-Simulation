function erf(x){
    var retval = 0.0;
    var neg = false;
    if (x < 0){
      neg = true;
      x = (-1)*x;
    } 
    var dx = x/1000;
    for(var i = 0; i < x; i = i + dx){
      retval += dx * Math.exp(-1*(i**2));
    }
    retval = retval*2/Math.sqrt(Math.PI);
    if (retval > 1){
      retval = 1.0;
    }
    if (neg){
      retval = (-1)*retval;
    }
    return retval;
}

function A (alpha, vw, x) {
    return 1/(2*alpha*Math.sqrt(Math.PI))*(-Math.exp(-1*(alpha*(vw+x))**2))
}
function B (alpha, vw, x) {
    return 1/2*(erf(alpha*(vw+x))-1)
}
function f(alpha, vw, x) {
// console.log("in f",x, A(alpha, vw, x), B(alpha, vw, x));
    return A(alpha, vw, x) - vw * B(alpha, vw, x)
}
function F(alpha, vw, x) {
// console.log("in F", x, f(alpha,vw, x), f(alpha, vw, 0))
    return 1-(f(alpha,vw,x)/f(alpha, vw, 0));
}
function Finv(F, alpha, vw, y){
    x = 0
    dx = 1
    transition = [false, false]
    error = y - F(alpha, vw, x)
    // console.log("F(alpha, vw, x)", F(alpha, vw, x));
    // console.log("error", error);
    while (abs(error) > 1e-9) {
        // console.log(x, "error", error);
        if (error > 0) {
            // print("error > 0");
            transition[0] = true
            x = x + dx;
            // print("y", y,"x", x, "alpha", alpha);
            // print("check", error, y - F(alpha, vw, x));
            // print("check", y - F(alpha, vw, 0), y - F(alpha, vw, 1), y - F(alpha, vw, 2), y - F(alpha, vw, 300000));
            // print(F(alpha, vw, 0), F(alpha, vw, 1), F(alpha, vw, 2), F(alpha, vw, 300000))
        }
        if (error < 0) {
            // print("error < 0");
            transition[1] = true
            x = x - dx;
            // print("x", x)
            // print("check", error, y - F(alpha, vw, x));
            // print("check", y - F(alpha, vw, 0), y - F(alpha, vw, 1), y - F(alpha, vw, 2), y - F(alpha, vw, 3));
        }
        if (transition[0] && transition[1]) {
            dx = dx * 0.1;
            transition = [false, false];
        }
        if (error == y - F(alpha, vw, x)) {
            break;
        }
        error = y - F(alpha, vw, x);
    }
    return x
}
function erfc(x) {
    return 1-erf(x);
}
function collision2d(ma, mb, vax, vbx, vay, vby, sin, cos){
    var e = 1;
    vaxp = (ma-e*mb)/(ma+mb)*(vax*cos+vay*sin)+(mb+e*mb)/(ma+mb)*(vbx*cos+vby*sin)
    vbxp = (ma+e*ma)/(ma+mb)*(vax*cos+vay*sin)+(mb-e*ma)/(ma+mb)*(vbx*cos+vby*sin)
    vayp = vay*cos - vax*sin
    vbyp = vby*cos - vbx*sin
    
    vaxp2 = vaxp*cos-vayp*sin
    vayp2 = vaxp*sin+vayp*cos
    vbxp2 = vbxp*cos-vbyp*sin
    vbyp2 = vbxp*sin+vbyp*cos
    
    return [vaxp2, vbxp2, vayp2, vbyp2]
}
function calculate_particles_collision(fp, mp){

    var collision_check = false;
    var new_fp_x = fp.x;
    var new_fp_y = fp.y;
    var new_fp_vx = fp.vx;
    var new_fp_vy = fp.vy;
    var new_mp_vx = mp.vx;
    var new_mp_vy = mp.vy;
    
    var dx = fp.x-mp.x;
    var dy = fp.y-mp.y;
    if (dx*dx+dy*dy < mp.r/2*mp.r/2){
        collision_check = true;
        var col_angle_sin = dy/sqrt(dx*dx+dy*dy);
        var col_angle_cos = dx/sqrt(dx*dx+dy*dy);
        list_v = collision2d(mp.mass, fp.mass, mp.vx, fp.vx, mp.vy, fp.vy, col_angle_sin, col_angle_cos);
        new_mp_vx = list_v[0];
        new_fp_vx = list_v[1];
        new_mp_vy = list_v[2];
        new_fp_vy = list_v[3];      
        new_fp_y = mp.y  + col_angle_sin*(mp.r/2);
        new_fp_x = mp.x  + col_angle_cos*(mp.r/2);
    }

    return [collision_check,new_mp_vx,new_mp_vy,new_fp_x,new_fp_y,new_fp_vx,new_fp_vy];
}
function check_remove_paricle(fp, mp, window_height, window_width){
    // calculate coodinate
    var fp_coord_x = fp.x+window_width/2-mp.x
    var fp_coord_y = fp.y+window_height/2-mp.y
    
    // remove the out of window
    if (fp_coord_x < 0 || fp_coord_x > window_width || fp_coord_y < 0 || fp_coord_y > window_height){
        return true;
    }else{
        return false;
    }
} 
function calculate_paticles_to_add1(mp, fp_m, density, dt, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left){
    var a = 2*fp_m*k*T
    
    // added particle parts  
    var num_new_particles_from_bottom = 0.0;
    for (s = -1*int(mp.vy); s < -1*int(mp.vy)+10000; s++) {
          num_new_particles_from_bottom = num_new_particles_from_bottom + (s+mp.vy)*exp(-1*pow(s,2)/a);
    }
    var num_new_particles_from_top =  0.0;
    for (s = -100000-1*mp.vy; s < -1*mp.vy; s++){ 
          num_new_particles_from_top = num_new_particles_from_top + (abs(s+mp.vy))*exp(-1*pow(s,2)/a);
    }
    var num_new_particles_from_right = 0.0;
    for (s = -1*int(mp.vx); s < -1*int(mp.vx)+10000; s++) {
          num_new_particles_from_right = num_new_particles_from_right + (s+mp.vx)*exp(-1*pow(s,2)/a);
    }
    var num_new_particles_from_left =  0.0;
    for (s = -100000-1*mp.vx; s < -1*mp.vx; s++){ 
          num_new_particles_from_left = num_new_particles_from_left + (abs(s+mp.vx))*exp(-1*pow(s,2)/a);
    }
    
    
    num_bottom = num_bottom +(num_new_particles_from_bottom)*density*dt*window_width/sqrt(T);
    num_top = num_top + (num_new_particles_from_top)*density*dt*window_width/sqrt(T);
    num_right = num_right +(num_new_particles_from_right)*density*dt*window_height/sqrt(T);
    num_left = num_left + (num_new_particles_from_left)*density*dt*window_height/sqrt(T);

    if (num_bottom > 0 ){
        for(var i = 0; i < int(num_bottom); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, false, "bottom"));
        }
        num_bottom = num_bottom - int(num_bottom)
    }
    if (num_top > 0 ){
        for(var i = 0; i < int(num_top); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, false, "top"));
        }
        num_top = num_top - int(num_top)        
    }
    if (num_right > 0 ){
        for(var i = 0; i < int(num_right); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, false, "right"));
        }
        num_right = num_right - int(num_right)
        
    }
    if (num_left > 0 ){
        for(var i = 0; i < int(num_left); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, 1, mp, false, "left"));
        }
        num_left = num_left - int(num_left)
    }

    return [num_bottom, num_top, num_right, num_left]
}
function calculate_paticles_to_add(mp, fp_m, fp_r, density, dt, g, T, window_width, window_height, num_bottom, num_top, num_right, num_left){
    var a = Math.sqrt(2*k*T/fp_m);
    var vwx = mp.vx;      // - : windonw move left (particle right), + : windonw move right (particle left)
    var vwy = mp.vy;      // + : windonw move top (particle bottom), - : windonw move bottom (particle top)


    dnum_right   = density * sqrt((2*k*T)/(fp_m)) * dt / 2 * (Math.exp(-1*(vwx/a)**2)/sqrt(Math.PI) +(vwx/a)*erfc((-1)*vwx/a)) * window_height;
    dnum_left    = density * sqrt((2*k*T)/(fp_m)) * dt / 2 * (Math.exp(-1*(vwx/a)**2)/sqrt(Math.PI) -(vwx/a)*erfc(vwx/a)) * window_height;
    dnum_bottom  = density * sqrt((2*k*T)/(fp_m)) * dt / 2 * (Math.exp(-1*(vwy/a)**2)/sqrt(Math.PI) +(vwy/a)*erfc((-1)*vwy/a)) * window_width;
    dnum_top     = density * sqrt((2*k*T)/(fp_m)) * dt / 2 * (Math.exp(-1*(vwy/a)**2)/sqrt(Math.PI) -(vwy/a)*erfc(vwy/a)) * window_width;

    num_right   += round(dnum_right, 9);
    num_left    += round(dnum_left, 9);
    num_bottom  += round(dnum_bottom, 9);
    num_top     += round(dnum_top, 9);

    if (num_bottom > 0 ){
        for(var i = 0; i < int(num_bottom); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "bottom", vwx, vwy));
        }
        num_bottom = num_bottom - int(num_bottom);
    }
    if (num_top > 0 ){
        for(var i = 0; i < int(num_top); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "top", vwx, vwy));
        }
        num_top = num_top - int(num_top);
        
    }
    if (num_right > 0 ){
        for(var i = 0; i < int(num_right); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "right", vwx, vwy));
        }
        num_right = num_right - int(num_right);
    }
    if (num_left > 0 ){
        for(var i = 0; i < int(num_left); i++){
            fps.push(new free_particle(window_width, window_height, g, dt, fp_m, fp_r, T, k, mp, "left", vwx, vwy));
        }
        num_left = num_left - int(num_left);
        
    }

    return [num_bottom, num_top, num_right, num_left]
}