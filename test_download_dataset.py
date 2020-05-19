import cwru
database = cwru.CWRU()
# import paderborn
# database = paderborn.Paderborn()

database.download()
database.segmentate()
