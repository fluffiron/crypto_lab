from Crypto.Cipher import AES
from Crypto import Random
from re import  search

class PKCS7Exception(Exception):
	pass

def addition_PKCS7(in_str, req_len):
	num = req_len - len(in_str)
	return in_str + "".join( chr(num) for i in range(num) )


def PKCS7_decode(in_str):
	padd_len = ord(in_str[ len(in_str) - 1 ])
	padding = in_str[-padd_len:]
	for byte in padding:
		if ord(byte) != padd_len:
			raise PKCS7Exception("Wrong format")
	return in_str[:-padd_len]


def change_byte(plain_text, encrypted_data,cipher):
	index_brute = plain_text.find("^") - AES.block_size
	for byte in range(256):
		attack_encrypted_data = encrypted_data[:index_brute] + chr(byte) + encrypted_data[index_brute + 1:]
		attack_plain_text = cipher.decrypt(attack_encrypted_data)

		if attack_plain_text.find("admin=true") != -1:
			print(attack_plain_text)
			return True
	return False

def formating(in_str):
	return "comment1=cooking%20MCs;userdata=" + in_str.replace("=", "").replace(";","") + "comment2=%20like%20a%20pound%20of%20bacon"

key = Random.new().read(AES.block_size)
iv = "\x00" * 16
user_data = "admin^true"

cipher = AES.new(key, AES.MODE_CBC, iv)

open_text = formating(user_data)
if len(open_text) % 16 != 0:
	open_text = addition_PKCS7(open_text, len(open_text) + 16 - len(open_text) % 16 )
msg_enc = cipher.encrypt(open_text)

change_byte(open_text, msg_enc, cipher)



