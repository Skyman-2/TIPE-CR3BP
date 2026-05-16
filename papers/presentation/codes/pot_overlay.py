def potential(x,y,system):
    orbital_radius = system["radius"]  # Distance moyenne Terre-Lune en m
    grav_potential_body1 = -1 * G*body1_mass/(distance(x,y,body1_pos))
    grav_potential_body2 = -1 * G*body2_mass/(distance(x,y,body2_pos))
    centrifugal_potential = -0.5 * omega(system)**2*(x**2+y**2)
    result = grav_potential_body1 + grav_potential_body2 + centrifugal_potential
    return result


def total_potential(system,surface,step):
    x = np.linspace(surface[0][0], surface[0][1], step)
    y = np.linspace(surface[1][0], surface[1][1], step)
    X,Y = np.meshgrid(x,y)
    Z = potential(X,Y,system)
    return (X,Y,Z)