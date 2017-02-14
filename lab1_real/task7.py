from Crypto.Cipher import AES
from Crypto import Random
import collections

def PKCS7_decode(in_str):
	padd_len = ord(in_str[ len(in_str) - 1 ])
	padding = in_str[-padd_len:]
	for byte in padding:
		if ord(byte) != padd_len:
			raise PKCS7Exception("Wrong format")
	return in_str[:-padd_len]

def addition_PKCS7(in_str):
	if len(in_str) % 16 != 0:
		req_len = len(in_str) + 16 - len(in_str) % 16
	else:
		req_len = len(in_str)
	num = req_len - len(in_str)
	return in_str + "".join( chr(num) for i in range(num) )

class my_AES():
	cipher = None
	def __init__(self):
		key = Random.new().read(AES.block_size)
		self.cipher = AES.new(key, AES.MODE_ECB)

a=my_AES()
