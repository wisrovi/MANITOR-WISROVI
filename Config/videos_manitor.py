def CreateInstruccion(path_video, id, name="paso"):
    inst = dict()
    inst['path'] = path_video
    inst['name'] = name + " " + str(id)
    inst['id'] = id
    return inst


def CreateGuion(id, text):
    guion = dict()
    guion['id'] = id
    guion['text'] = text
    return guion

from Config.Constantes.pantallas import PANTALLAS
SCREEN = "RPI"
LIENZO_MOSTRAR_VIDEOS = ( PANTALLAS[SCREEN][1], PANTALLAS[SCREEN][0]) # pixeles (alto, largo)


PATH_VIDEOS = "resources/"


INSTRUCCIONES = list()
INSTRUCCIONES.append(  CreateInstruccion(id=0, path_video='0_bienvenida.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=1, path_video='1_mojarse_manos.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=2, path_video='2_aplique_jabon.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=3, path_video='3_palma_con_palma.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=4, path_video='5_detras_manos.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=5, path_video='4_entre_dedos.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=6, path_video='7_detras_dedos.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=7, path_video='6_pulgares.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=8, path_video='8_unas.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=9, path_video='9_munecas.mp4')  )
INSTRUCCIONES.append(  CreateInstruccion(id=10, path_video='10_enjuagarSecar.mp4')  )


GUIONES = list()
GUIONES.append( CreateGuion(id=0, text="Bienvenido al sistema integrado de lavado de manos. A continuación daré unas instrucciones las cuales debe seguir para un correcto lavado de manos.") )
GUIONES.append( CreateGuion(id=1, text="Primero, moje ambas manos con suficiente agua. "))
GUIONES.append( CreateGuion(id=2, text="Segundo, aplique suficiente jabón sobre la superficie de la palma de la mano."))
GUIONES.append( CreateGuion(id=3, text="Tercero, frote ambas palmas de las manos."))
GUIONES.append( CreateGuion(id=4, text="Cuarto, frote el dorso de cada mano con la palma de la otra mano, teniendo los dedos entrelazados."))
GUIONES.append( CreateGuion(id=5, text="Quinto, frote ambas palmas de las manos con los dedos entrelazados."))
GUIONES.append( CreateGuion(id=6, text="Sexto, frote con el dorso de los dedos las palmas de la manos, teniendo los dedos entrelazados."))
GUIONES.append( CreateGuion(id=7, text="Séptimo, presione y rote cada dedo pulgar con la mano opuesta."))
GUIONES.append( CreateGuion(id=8, text="Octavo, frote las puntas de los dedos con la palma opuesta teniendo un movimiento circular"))
GUIONES.append( CreateGuion(id=9, text="Noveno, frote cada muñeca con la mano opuesta."))
GUIONES.append( CreateGuion(id=10, text="Decimo, enjuague sus manos con suficiente agua."))


# !Nota:
# los videos no pueden superar el tiempo en 'TIEMPO_POR_INSTRUCCION', este es el tiempo maximo por video, se recomienda no mayor al 80% de esta variable


