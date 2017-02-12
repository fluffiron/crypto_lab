from Crypto.Cipher import AES
from hashlib import md5


def original_key(key_string, salt, key_length):
	sum_digest = ""
	while len(sum_digest) < key_length + AES.block_size:
		sum_digest += md5(sum_digest + key_string + salt).digest()
	return sum_digest[:key_length]

with open("decryptAesEcb.txt") as f:
	content = f.readlines()
input_str = ""
for x in content:
	input_str += x.strip()


key = "YELLOW SUBMARINE"

key = original_key(key, input_str.decode("base64")[:AES.block_size][len('Salted__'):],len(key))

cipher = AES.AESCipher(key, AES.MODE_ECB)
print(cipher.decrypt( input_str.decode("base64") ))
