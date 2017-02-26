from Crypto.Cipher import AES
from Crypto import Random


class Counter:
	def __init__(self, nonce=0, initial_value=0):
		self.__nonce = chr(nonce) * 8
		self.__val = initial_value - 1
	
	def counter(self):
		self.__val += 1
		return self.__nonce + self.__int_to_l_endian_64_bit( self.__val ) 
	
	def __int_to_l_endian_64_bit(self,int_val):
		res_str = ""
		for i in range(8):
			res_str += chr(int_val & 0xff)
			int_val >>= 8
		return res_str

key = Random.new().read(AES.block_size)
str_file = open("input_strings.txt")

encrypted_lines = []
for line in str_file:
	cnt_decrypt = Counter(0,0)
	cipher = AES.new(key, AES.MODE_CTR, counter=cnt_decrypt.counter)
	encrypted_lines.append(cipher.encrypt(line.decode("base64")))

																																																																																																																																																																																																																						
																																																																																																																																																																																																																																																																																																			
