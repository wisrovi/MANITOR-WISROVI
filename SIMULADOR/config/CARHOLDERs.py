ID_ESP = list()  ## mac junto al ID_ESP entran a una ecuacion y sale este valor
ID_ESP.append("111111AAAAAA")
ID_ESP.append("111111BBBBBB")
ID_ESP.append("111111CCCCCC")
ID_ESP.append("111111DDDDDD")

ALL_CARD_HOLDER = list()
FCV = "00706786" # http://1.bp.blogspot.com/-gTya0k5EPtY/UlsYUkVM-HI/AAAAAAAAAIg/YeMEivnolAY/s1600/IMAGEN13.jpg
LOTE = "0001"  # lote fabricación
LV = str(int( float(3.6) * 1000 )) # nivel de bateria del cardholder
for i, id in enumerate(ID_ESP):
    uuid = FCV + "-" + LOTE +  "-" + LV +  "-0000-" + id
    ALL_CARD_HOLDER.append(uuid)

ALL_CARD_HOLDER.append("00706786-0001-447a-acb1-ce7451b5beef")
ALL_CARD_HOLDER.append("00706786-0001-3600-0000-111111CCCCCC")

# print(ALL_CARD_HOLDER)