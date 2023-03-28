use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (pos_vel, g, c, mass, max_iter=5))]
fn post_newt_diff_eq(pos_vel: Vec<Vec<f64>>, g: f64, c: f64, mass: Vec<f64>, max_iter: usize) -> PyResult<Vec<Vec<f64>>> {
    let mut out = vec![];
    let n: usize = pos_vel.len();

    for line in &pos_vel {
        out.push(vec![line[3], line[4], line[5], 0.0, 0.0, 0.0])
    }

    let mut iteration: usize = 0;

    while iteration < max_iter {
        iteration += 1;
        let mut acc: Vec<Vec<f64>> = vec![];
        for _ in 0..n {
            acc.push(vec![0.0, 0.0, 0.0]);
        }

        for a in 0..n {
            for b in 0..n {
                if a == b {
                    continue;
                }

                let dist = distance(&pos_vel[a], &pos_vel[b]);
                let rad = radius(&dist);

                let mut inner1 = 0.0;
                for c in 0..n {
                    if c == a {
                        continue;
                    }
                    inner1 += -4.0 * g * mass[c] / radius(&distance(&pos_vel[a], &pos_vel[c]))
                }

                let mut inner2 = 0.0;
                for c in 0..n {
                    if c == b {
                        continue;
                    }
                    inner2 -= g * mass[c] / radius(&distance(&pos_vel[b], &pos_vel[c]))
                }

                for coordinate in 0..3 {
                    acc[a][coordinate] += g * mass[b] * dist[coordinate] / rad.powi(3) *
                        (1.0
                            + 1.0 / c.powi(2) * (pos_vel[a][3].powi(2)
                            + pos_vel[a][4].powi(2)
                            + pos_vel[a][5].powi(2)
                            + 2.0 * (pos_vel[b][3].powi(2)
                            + pos_vel[b][4].powi(2)
                            + pos_vel[b][5].powi(2))
                            - 4.0 * (pos_vel[a][3] * pos_vel[b][3]
                            + pos_vel[a][4] * pos_vel[b][4]
                            + pos_vel[a][5] * pos_vel[b][5])
                            - 1.5 / rad.powi(2) * (dist[0] * pos_vel[b][3]
                            + dist[1] * pos_vel[b][4]
                            + dist[2] * pos_vel[b][5]).powi(2)
                            + inner1
                            + inner2
                            + 0.5 * (dist[0] * out[b][3]
                            + dist[1] * out[b][4]
                            + dist[2] * out[b][5])
                        )
                        );
                    acc[a][coordinate] += 1.0 / c.powi(2) * g * mass[b] / rad.powi(3)
                        * dist[coordinate]
                        * (4.0 * pos_vel[a][coordinate + 3] - 3.0 * pos_vel[b][coordinate + 3])
                        * (pos_vel[a][coordinate + 3] - pos_vel[b][coordinate + 3]);
                    acc[a][coordinate] += 3.5 / c.powi(2) * g * mass[b] / rad * out[b][coordinate + 3];
                }
            }
        }
        let done = true;

        for row in 0..n {
            for coord in 0..3 {
                if acc[row][coord] != out[row][coord+3] {
                    let done = false;
                }
                out[row][coord+3] = acc[row][coord];
            }
        }
        if done {
            iteration = max_iter;
        }
    }

    Ok(out)
}



fn distance(pos_a: &Vec<f64>, pos_b: &Vec<f64>) -> Vec<f64> {
    vec![pos_b[0] - pos_a[0], pos_b[1] - pos_a[1], pos_b[2] - pos_a[2]]
}

fn radius(distance: &Vec<f64>) -> f64 {
    (distance[0].powi(2) + distance[1].powi(2) + distance[2].powi(2)).sqrt()
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustlib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(post_newt_diff_eq, m)?)?;
    Ok(())
}
