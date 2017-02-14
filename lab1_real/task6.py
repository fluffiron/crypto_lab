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

def dict_to_str(d):
	res_str = ""
	for key, value in d.items():
		res_str += str(key) + "=" + str(value) + "&"
	return res_str[:-1]

def str_to_dict(in_str):
	res_dict = collections.OrderedDict()
	lines = in_str.split("&")
	for line in lines:
		key_value = line.split("=")
		if len(key_value) == 2:
			res_dict[key_value[0]] = key_value[1]
		if len(key_value) == 1:
			res_dict[key_value[0]] = ""
	return res_dict

def profile_for(email):
	d_d = collections.OrderedDict()
	d_d["email"] = email
	d_d["uid"] = "10"
	d_d["role"] =  "user"
	return  dict_to_str(d_d)

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

cipher_text = a.cipher.encrypt( addition_PKCS7( profile_for("f@bar.com") ) )
#print [line[i:i+16] for i in range(0,len(line),16)]
part_crypt = a.cipher.encrypt(addition_PKCS7("uid=10&role=admin"))

res_cip = cipher_text[:16] + part_crypt
print str_to_dict(PKCS7_decode(a.cipher.decrypt(res_cip)))
