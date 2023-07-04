use std::{fs, collections::HashMap};

fn read_input() -> String {
    let contents = fs::read_to_string("data.txt")
        .expect("Should have been able to read file");

    return contents;
}

// fn printv(p: (i32,i32)) {
//     println!("({},{})", p.0, p.1);
// }
fn rotate_r(p : (i32,i32)) -> (i32,i32) {
    /*
     * [ 0 1]*[x] = [0 + y]
     * [-1 0] [y]   [-x +  0]
     */
    return (p.1,-1*p.0);
}
fn rotate_l(p : (i32,i32)) -> (i32,i32) {
    /*
     * [0 -1]*[x] = [0 + -y]
     * [1  0] [y]   [x +  0]
     */
    return (-1*p.1,p.0);
}

fn do_move(p: (i32,i32), d:(i32,i32), m: i32) -> (i32, i32) {
    return (p.0 + d.0*m, p.1 + d.1*m);
}

fn get_answer() {
    let mut d = (0, 1);

    let mut p = (0, 0);


    read_input()
        .replace("\n", "")
        .replace("\r", "")
        .split(", ")
        .for_each(|val| {
            let (dir,sn) = val.split_at(1);
            let n = sn.parse::<i32>().unwrap();
            match dir {
                "L" => {
                    d = rotate_l(d);
                    p = do_move(p, d, n);
                },
                "R" => {
                    d = rotate_r(d);
                    p = do_move(p, d, n);
                },
                _ => print!("WHAT? {},{}", dir, n),
            };
            
        });
    
    println!("{} dist", p.0.abs() + p.1.abs());
}

fn get_answer2() {
    let mut m = HashMap::new();
    let mut d = (0, 1);

    let mut p = (0, 0);

    m.insert(p, 1);

    let mut stop = false;

    read_input()
        .replace("\n", "")
        .replace("\r", "")
        .split(", ")
        .for_each(|val| {
            if stop {
                return;
            }
            let (dir,sn) = val.split_at(1);
            let n = sn.parse::<i32>().unwrap();
            match dir {
                "L" => {
                    d = rotate_l(d);
                },
                "R" => {
                    d = rotate_r(d);
                },
                _ => print!("WHAT? {},{}", dir, n),
            };
            for _ in 0..n {
                
                p = do_move(p, d, 1);
            
                if m.contains_key(&p) {
                    stop = true;
                    break;
                } else {
                    m.insert(p, 1);
                }
            }
        });
    
    println!("{} dist at {},{}", p.0.abs() + p.1.abs(), p.0, p.1);
}

fn main() {
    get_answer();
    get_answer2();

}
