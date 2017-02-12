from Crypto.Cipher import AES
from Crypto import Random
from random import randint


def addition_PKCS7(in_str, req_len):
	num = req_len - len(in_str)
	return in_str + "".join( chr(num) for i in range(num) )

def is_repeat_blocks(cipher_text):
	blocks = [cipher_text[i:i+16] for i in range(0, len(cipher_text), 16)]
	if len(set(blocks)) != len(blocks):
		return True
	return False

def encryption_oracle(input_str):
	suffix = Random.new().read(10)
	preffix = Random.new().read(6)
	input_str = suffix + input_str + preffix
	key = Random.new().read( AES.block_size )
	if randint(0,1)  == 1:
		cipher = AES.new(key, AES.MODE_ECB)
	else:
		cipher = AES.new(key, AES.MODE_CBC,"\x00" * 16 )
	return cipher.encrypt(addition_PKCS7(input_str, len(input_str) + 16 - len(input_str) % 16 ))

def detect_mode(test_cnt=10, n_blocks=7):
	open_text = chr(randint(0,255)) * 16 * n_blocks
	for i in range(test_cnt):
		cipher_text = encryption_oracle(open_text)
		if is_repeat_blocks(cipher_text):
			print "It's ECB probably"
		else:
			print "It's CBC maybe"


detect_mode(11,10)

