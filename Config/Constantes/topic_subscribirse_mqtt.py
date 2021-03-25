from Util.util import Get_MAC

PROJECT = "/SPINPLM/"

TOPICS_USAR = list()
TOPICS_USAR.append(PROJECT + "restart")
TOPICS_USAR.append(PROJECT + "OTA")
TOPICS_USAR.append(PROJECT + Get_MAC() + "/restart" )
TOPICS_USAR.append(PROJECT + Get_MAC() + "/OTA" )