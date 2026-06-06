def potentiel(x,y,systeme):
    grav_potential_body1 = -1 * G*masse_corps1/(distance(x,y,position_corps1))
    grav_potential_body2 = -1 * G*masse_corps2/(distance(x,y,position_corps2))
    potentiel_centrifuge = -0.5 * omega**2*(x**2+y**2)
    resultat = grav_potential_body1 + grav_potential_body2 + potentiel_centrifuge
    return resultat


def potentiel_total(systeme,surface,pas):
    x = np.linspace(surface[0][0], surface[0][1], pas)
    y = np.linspace(surface[1][0], surface[1][1], pas)
    X,Y = np.meshgrid(x,y)
    Z = potentiel(X,Y,systeme)
    return (X,Y,Z)
