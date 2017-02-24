from Crypto.Cipher import AES
from Crypto import Random
from random import randint

unknownStrBase64="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

def PKCS7_decode(in_str):
	padd_len = ord(in_str[ len(in_str) - 1 ])
	padding = in_str[-padd_len:]
	for byte in padding:
		if ord(byte) != padd_len:
			raise PKCS7Exception("Wrong format")
	return in_str[:-padd_len]

def addition_PKCS7(in_str, req_len=16):
	num = req_len - len(in_str) % req_len
	if num == 0:
		return in_str + "".join( chr(len(in_str)) for i in range(len(in_str)) )
	return in_str + "".join( chr(num) for i in range(num) )

class my_AES():
	cipher = None
	rand_str = ""
	def __init__(self):
		key = Random.new().read(AES.block_size)
		self.rand_str = Random.new().read(randint(1,255))
		self.cipher = AES.new(key, AES.MODE_ECB)
	def crypt(self, in_str):
		return self.cipher.encrypt(addition_PKCS7(self.rand_str + in_str + unknownStrBase64.decode("base64")))

a=my_AES()


def brute_force():
	block_size = 16
	blocks_n = len(a.crypt(""))/16
	
	cip_AA = a.cipher.encrypt("A" * 16)[:16]
	addit_str = ""
	beginning = 0
	for j in range(16,32):
		tmp_str = "A" * j
		cip_t = a.crypt(tmp_str)
		l_tmp = [cip_t[i:i+16] for i in range(0, len(cip_t), 16)]
		if l_tmp.count(cip_AA) > 0:
			addit_str = "A" * j
			beginning = ( l_tmp.index(cip_AA) + 1)* 16
#			print l_tmp.index(cip_AA)
			blocks_n -= l_tmp.index(cip_AA)
			break			
		
	open_text = ""
	cnt_blocks = 0
	
	while cnt_blocks < blocks_n:
		tmp_open_str = ""
		for l in range(block_size - 1, -1, -1):
			if cnt_blocks == 0 or l == 0:
				my_str = "A" * l
			else:
				my_str = open_text[-16 + ( 16 - l ):]
			ciph = a.crypt( addit_str + "A" * l  )[beginning:]
			for byte in range(256):
				if len(my_str + tmp_open_str) + 1 != 16:
					break
				if a.cipher.encrypt(my_str + tmp_open_str + chr(byte)) == ciph[16 * cnt_blocks :block_size + 16 * cnt_blocks]:
					tmp_open_str += chr(byte)
					break
		open_text += tmp_open_str
		cnt_blocks += 1
							
		
	return open_text[:-1]



print brute_force()
