from Crypto.Cipher import AES
from Crypto import Random


unknownStrBase64="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

def addition_PKCS7(in_str):
	req_len = len(in_str) + 16 - len(in_str) % 16
	num = req_len - len(in_str)
	return in_str + "".join( chr(num) for i in range(num) )

def is_repeat_blocks(cipher_text):
	blocks = [cipher_text[i:i+16] for i in range(0, len(cipher_text), 16)]
	if len(set(blocks)) != len(blocks):
		return True
	return False

class my_AES():
	cipher = None
	def __init__(self):
		key = Random.new().read(AES.block_size)
		self.cipher = AES.new(key, AES.MODE_ECB)
	
	def crypt(self, str_r):
		return self.cipher.encrypt(addition_PKCS7( str_r + unknownStrBase64.decode("base64") ))

a=my_AES()

def brute_force():
	block_size = 0
	for l in range(1,35):
		my_str = "A" * l
		ciph = a.cipher.encrypt(addition_PKCS7( my_str ))
		if is_repeat_blocks(ciph):
			block_size = l / 2
			break
	blocks_n = len(a.crypt(""))/16
	open_text = ""
	cnt_blocks = 0
	while cnt_blocks < blocks_n:
		tmp_open_str = ""
		for l in range(block_size - 1, -1, -1):
			if cnt_blocks == 0 or l == 0:
				my_str = "A" * l
			else:
				my_str = open_text[-16 + ( 16 - l ):]
			ciph = a.crypt( "A" * l  )
			for byte in range(256):
				if len(my_str + tmp_open_str) + 1 != 16:
					tmp_open_str = tmp_open_str[:-1]
					break
				if a.cipher.encrypt(my_str + tmp_open_str + chr(byte)) == ciph[16 * cnt_blocks :block_size + 16 * cnt_blocks]:
					tmp_open_str += chr(byte)
					break
		open_text += tmp_open_str
		cnt_blocks += 1
							
		
	return open_text
		

my_str = "dddddddddddddddd"
#print a.cipher.encrypt(addition_PKCS7( my_str + unknownStrBase64.decode("base64")))
print(brute_force())


#print unknownStrBase64.decode("base64")
