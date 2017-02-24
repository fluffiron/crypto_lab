from random import randint
from Crypto.Cipher import AES
from Crypto import Random

strings = [ \
"V2l0aCB5b3VyIGZlZXQgaW4gdGhlIGFpciBhbmQgeW91ciBoZWFkIG9uIHRoZSBncm91bmQK", \
"VHJ5IHRoaXMgdHJpY2sgYW5kIHNwaW4gaXQhIFllYWhoIQo=", \
"WW91ciBoZWFkIHdpbGwgY29sbGFwc2UsIGJ1dCB0aGVyZSdzIG5vdGhpbmcgaW4gaXQK", \
"QW5kIHlvdSdsbCBhc2sgeW91cnNlbGY/Cg==", \
"V2hlcmUgaXMgbXkgbWluZD8K", \
"V2F5IG91dCwgaW4gdGhlIHdhdGVyIHNlZSBpdCBzd2ltbWluJyAK", \
"SSB3YXMgc3dpbW1pbicgaW4gdGhlIENhcnJpYmVhbgo=", \
"QW5pbWFscyB3b3VsZCBoaWRlIGJlaGluZCB0aGUgcm9ja3MuIFllYWhoIQo=", \
"RXhjZXB0IHRoZSBsaXR0bGUgZmlzaAo=", \
"QnV0IGhlIHRvbGQgbWUgZWFzdCB3YXMgd2VzdAo=", \
"VHJ5aW4nIHRvIHRhbGsgCg==" \
]

def PKCS7_decode(in_str):
	padd_len = ord(in_str[ len(in_str) - 1 ])
	padding = in_str[-padd_len:]
	for byte in padding:
		if ord(byte) != padd_len:
			raise PKCS7Exception("Wrong format")
	return in_str[:-padd_len]

def addition_PKCS7(in_str, block_size=16):
	num = block_size - len(in_str) % block_size
	return in_str + "".join( chr(num) for i in range(num) )

class my_AES():
	cipher = None
	def __init__(self):
		self.key = Random.new().read(AES.block_size)
		self.cipher = AES.new(self.key, AES.MODE_CBC,"\x00" * 16 )
	def crypt(self):
		str_to_crypt = strings[randint( 0 , len(strings) - 1)].decode("base64")
		return self.cipher.encrypt(addition_PKCS7( str_to_crypt ))
	def decrypt (self,in_str, ivv):
		self.cipher = AES.new(self.key, AES.MODE_CBC, ivv )
		op_t = self.cipher.decrypt(in_str)
		try:
			PKCS7_decode(op_t)
		except:
			return False
		#print op_t
		return True

a=my_AES()

def get_trail_prev_block(interm_state, req_char):
	return "".join( chr(ord(char) ^ req_char) for char in interm_state )
	

def CBC_padd_oracle():
	ivv = "\x00" * 16
# getting cipher text
	cip_t = a.crypt()	
	blocks = [cip_t[i:i + 16] for i in range(0, len(cip_t), 16)]
	decrypting_block_num = len(blocks) - 1
	open_text = ""
#decrypting start
	while decrypting_block_num >= 0:
		if decrypting_block_num != 0:
			prev_block = blocks[decrypting_block_num - 1]
		else:
			prev_block = ivv

		intermediate_state = ""
		for place in range(15, -1, -1):
			true_resp = []	
			for ch in range(256):
				changed_prev_block = prev_block[ :place ] + chr(ch) + prev_block[place + 1:]
				if decrypting_block_num > 0:
					inp_str = "".join(blocks[:decrypting_block_num - 1]) + changed_prev_block + \
						"".join(blocks[decrypting_block_num :])
					response = a.decrypt( inp_str, "\x01" * 16 )
				else:
					inp_str = cip_t[:16]
					response = a.decrypt( inp_str, changed_prev_block)
				if response == True:
					true_resp.append(ch)
			if len(true_resp) == 1:			
				correct_byte = true_resp[0]
			if len(true_resp) > 1:
				for byte in true_resp:
					cnt = 0
					for prev_byte in range(256):
						changed_prev_block = prev_block[ :place - 1 ] + chr(prev_byte) + \
							chr(byte) + prev_block[place + 1:]
						if decrypting_block_num > 0:
							inp_str = "".join(blocks[:decrypting_block_num - 1]) + changed_prev_block + \
								"".join(blocks[decrypting_block_num :])
							response = a.decrypt( inp_str, "\x00" * 16 )
						else:
							inp_str = cip_t[:16]
							response = a.decrypt( inp_str, changed_prev_block)
						if response == False:
							break
						cnt += 1
					if cnt == 256:
						correct_byte = byte
						break
			
					
			intermediate_state = chr(correct_byte ^ (16 - place)) + intermediate_state
			open_text = chr( correct_byte ^ (16 - place) ^ ord(prev_block[place]) ) + open_text
			prev_block = prev_block[:place] + get_trail_prev_block( intermediate_state, 16 - place + 1 )
				
		blocks.pop()
		decrypting_block_num -= 1
	return PKCS7_decode(open_text)

print CBC_padd_oracle()



