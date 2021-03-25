from Config.videos_manitor import GUIONES, PATH_VIDEOS
from gtts import gTTS

dialogos = [diag['text'] for diag in GUIONES]

for i, dial in enumerate(dialogos):
    tts = gTTS(dial, lang='es-us')

    NOMBRE_ARCHIVO = PATH_VIDEOS + "p" + str(i) + ".mp3"
    with open(NOMBRE_ARCHIVO, "wb") as archivo:
        tts.write_to_fp(archivo)
        print("archivo guardado", NOMBRE_ARCHIVO)

# Luego de creados los archivos se deben convertir a .wav
# se puede usar por ejemplo: https://audio.online-convert.com/es/convertir-a-wav
