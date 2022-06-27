from random import randint

def encrypt(stringa) -> str:
	traslata = ''.join([chr(ord(i) + 3) for i in stringa])
	traslata_e_condita = ''.join([i + chr(randint(0,1000000)) for i in traslata])
	return traslata_e_condita

def decrypt(stringa) -> str:
	scondita = stringa[::2]
	scondita_e_traslata = ''.join([chr(ord(i) - 3) for i in scondita])
	return scondita_e_traslata

