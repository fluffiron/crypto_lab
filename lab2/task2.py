from Crypto.Cipher import AES

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
		 

cipher_text = "Or6kII/NM5bDyWwvTGC3B6KFCPz9H2Cxvakxs/uGFmENxPykZx4XJqb62VPGj6rj7w=="

key="YELLOW SUBMARINE"
nonce = 0
cnt_decrypt = Counter(0,0)
cipher = AES.new(key, AES.MODE_CTR, counter=cnt_decrypt.counter)
print cipher.decrypt(cipher_text.decode("base64"))
#cipher_blocks = [cipher_text[i:i+16] for i in range(0, len(cipher_text), 16)]

#cnt = 0
#for i in range(len( cipher_blocks )):
#	pass

#print str(crypto.decrypt(cipher_text.decode("base64")))
