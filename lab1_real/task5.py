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

a=my_AES()

def brute_force():
	block_size = 0
	for l in range(1,35):
		my_str = "A" * l
		ciph = a.cipher.encrypt(addition_PKCS7( my_str ))
		if is_repeat_blocks(ciph):
			block_size = l / 2
			break
	my_str = "A" * (block_size - 1)
	
	return block_size
		

my_str = "dddddddddddddddd"
#print a.cipher.encrypt(addition_PKCS7( my_str + unknownStrBase64.decode("base64")))
print(brute_force())



