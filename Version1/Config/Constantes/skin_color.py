import numpy as np


def CreateColor(h=0, s=0, v=0):
    # HSV -> H[0 a 179], S[0 a 255], V[0 a 255]
    return np.array([h, s, v])


colores = {  # rango de colores (minimo, maximo)
    'verde': (CreateColor(34, 177, 76), CreateColor(255, 255, 255)),
    'piel': (CreateColor(0, 48, 40), CreateColor(60, 255, 255)),
}

franja_colores = {
    "min": colores["piel"][0],
    "max": colores["piel"][1]
}
