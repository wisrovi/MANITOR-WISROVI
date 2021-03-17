from playsound import playsound

from Config.videos_manitor import PATH_VIDEOS, GUIONES

from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(1)

dialogos = None


def iniciar_sounds(path=None):
    global dialogos
    if path is None:
        path = PATH_VIDEOS
    dialogos = [path + "p" + str(id) + ".wav" for id in [diag['id'] for diag in GUIONES]]


def reproducir_audio(id_audio):
    if id_audio > len(dialogos):
        id_audio = len(dialogos)
    audio = dialogos[id_audio]
    playsound(audio)
    # print(audio)


def reproducir(id):
    currs = ThreadPoolExecutor(max_workers=5)
    currs.submit(reproducir_audio, id)
