import matplotlib.pyplot as plt
import numerical_trajectory as traj
import potential_calculations as u

def barycentre(m1,m2,r):
    return (m2*r)/(m1+m2)

def update_system(system):
    system["barycenter"] = barycentre(
        system["body1"]["mass"],
        system["body2"]["mass"],
        system["radius"]
    )


earth_moon_system = {
    "body1": {
        "name": "Earth",
        "mass": 5.972e24,  # kg
        "radius": 6.371e6  # m
    },
    "body2": {
        "name": "Moon",
        "mass": 7.34767309e22,  # kg
        "radius": 1.737e6  # m
    },
    "radius": 3.844e8
}
update_system(earth_moon_system)
print(earth_moon_system["barycenter"])

fig, ax = plt.subplots(figsize=(8, 8))


for i in range(2):
    traj.display_pretty_trajectory(
        traj.simulate_trajectory(
            [3.15e8+i*1e5,0.,0.,1e1], # initial conditions
            1e6, # simulation time
            10, # time step
            earth_moon_system
        ),
        earth_moon_system,
        ax,fig,
        display_precision = 10
    )

u.add_equipotential_contours(earth_moon_system,pmin=20,pmax=100,n_levels=100,alpha=0.3)

plt.savefig('destination_path.svg', format='svg', dpi=1200)
plt.show()
