
class Avatar_video:
    import numpy as np
    import cv2
    from Config.avatar import AVATAR
    from Config.videos_manitor import INSTRUCCIONES, LIENZO_MOSTRAR_VIDEOS


    instruccion_actual = 0
    avatar_inicio = True
    avatar = "Avatar"
    hay_video_mostrar = False
    video_instructivo_mostrar = "Objeto donde se guardaran los videos a mostrar, mas adelante se cambia al tipo de variable: cv2.VideoCapture('path')"

    path_video_actual = None
    multiplexor_avatar = True
    primer_inicio_avatar = False

    black_screen = None

    sistema_iniciado = False

    def __init__(self, path_videos=None):
        if path_videos is not None:
            self.PATH_VIDEOS = path_videos

        self.avatar = self.cv2.VideoCapture(self.PATH_VIDEOS + "/" + self.AVATAR['START'])
        self.black_screen = self.CrearFondoPonerVideos()

    def CrearFondoPonerVideos(self):
        black_screen = self.np.zeros([self.LIENZO_MOSTRAR_VIDEOS[0], self.LIENZO_MOSTRAR_VIDEOS[1], 3],
                                     dtype=self.np.uint8)  ## fondo donde poner el video

        return black_screen

    def CalcularNuevaDimension(self, actual, marco=0.8):
        deseado_0 = int(self.LIENZO_MOSTRAR_VIDEOS[0] * marco)
        deseado_1 = int(self.LIENZO_MOSTRAR_VIDEOS[1] * marco)

        dimen_0 = (deseado_0) / actual[0]
        dimen_1 = (deseado_1) / actual[1]

        nuevo_0 = int(actual[0] * dimen_0), int(actual[1] * dimen_0)
        nuevo_1 = int(actual[0] * dimen_1), int(actual[1] * dimen_1)

        if self.LIENZO_MOSTRAR_VIDEOS[0] >= nuevo_0[0] and self.LIENZO_MOSTRAR_VIDEOS[1] >= nuevo_0[1]:
            return dimen_0

        if self.LIENZO_MOSTRAR_VIDEOS[0] >= nuevo_1[0] and self.LIENZO_MOSTRAR_VIDEOS[1] >= nuevo_1[1]:
            return dimen_1

        return 1

    def proceso(self):
        if self.sistema_iniciado:
            if self.avatar_inicio:
                self.avatar_inicio, self.frame_avatar = self.avatar.read()
                if self.avatar_inicio:
                    self.frame_avatar = self.cv2.resize(self.frame_avatar, (self.LIENZO_MOSTRAR_VIDEOS[1], self.LIENZO_MOSTRAR_VIDEOS[0]))
                    self.black_screen = self.frame_avatar
                else:
                    self.avatar = self.cv2.VideoCapture(self.PATH_VIDEOS + "/" + self.AVATAR['BAS1'])
            else:
                if not self.primer_inicio_avatar:
                    self.primer_inicio_avatar = True
                    print("Inicio Avatar Completo")

                if self.hay_video_mostrar:
                    self.hay_video_mostrar, self.frame = self.video_instructivo_mostrar.read()
                    if self.hay_video_mostrar:
                        dimen = self.CalcularNuevaDimension(self.frame.shape, 0.7)
                        if dimen is not None:
                            self.frame = self.cv2.resize(self.frame, (0, 0), fx=dimen, fy=dimen)

                            origen_x = int(self.black_screen.shape[0] - self.frame.shape[0])
                            origen_x = origen_x - 50 if origen_x >= 50 else int(
                                (self.black_screen.shape[0] - self.frame.shape[0]) / 2)
                            origen_y = int((self.black_screen.shape[1] - self.frame.shape[1]) / 2)

                            self.black_screen[origen_x:self.frame.shape[0] + origen_x, origen_y:self.frame.shape[1] + origen_y] = self.frame
                else:
                    if not isinstance(self.avatar, str):
                        self.hay_avatar, self.frame_avatar = self.avatar.read()

                    if self.hay_avatar:
                        self.frame_avatar = self.cv2.resize(self.frame_avatar, (self.LIENZO_MOSTRAR_VIDEOS[1], self.LIENZO_MOSTRAR_VIDEOS[0]))
                        self.black_screen = self.frame_avatar
                    else:
                        self.multiplexor_avatar = False if self.multiplexor_avatar else True
                        self.avatar = self.cv2.VideoCapture \
                            (self.PATH_VIDEOS + "/" + self.AVATAR['BAS1']) if self.multiplexor_avatar else self.cv2.VideoCapture( self.PATH_VIDEOS + "/" + self.AVATAR['BAS2'])
        else:
            self.avatar_inicio = None
        return self.black_screen, self.avatar_inicio

    def terminar_proceso_avatar(self):
        self.instruccion_actual = 0
        self.avatar = self.cv2.VideoCapture(self.PATH_VIDEOS + "/" + self.AVATAR['END'])
        self.avatar_inicio = True

    def continuar_siguiente_paso_instruccion(self):
        self.path_video_actual = self.INSTRUCCIONES[self.instruccion_actual]['path']
        self.path_video_actual = self.PATH_VIDEOS + "/" + self.path_video_actual

        # print("nuevo video:", self.path_video_actual)
        try:
            self.video_instructivo_mostrar = self.cv2.VideoCapture(self.path_video_actual)
            self.hay_video_mostrar = True
        except:
            self.hay_video_mostrar = False

        self.instruccion_actual += 1

        return self.path_video_actual, self.instruccion_actual

    def cerrar_avatar(self):
        try:
            self.video_instructivo_mostrar.release()
            self.avatar.release()
        except:
            pass

    def get_primer_inicio_avatar(self):
        return self.primer_inicio_avatar

    def get_instruccion_actual(self):
        return self.instruccion_actual

    def iniciar_avatar(self):
        self.sistema_iniciado = True





