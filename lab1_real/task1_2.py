
class PKCS7Exception(Exception):
	pass

def addition_PKCS7(in_str, req_len):
	num = req_len - len(in_str)
	if num == 0:
		return in_str + "".join( chr(len(in_str)) for i in range(len(in_str)) )
	return in_str + "".join( chr(num) for i in range(num) )


def PKCS7_decode(in_str):
	padd_len = ord(in_str[ len(in_str) - 1 ])
	padding = in_str[-padd_len:]
	for byte in padding:
		if ord(byte) != padd_len:
			raise PKCS7Exception("Wrong format")
	return in_str[:-padd_len]
input_text = raw_input()

ff = addition_PKCS7(input_text , 20)
print ff
print PKCS7_decode(ff)
'''
print( PKCS7_decode(addition_PKCS7(input_text, 20)))
try:
	print(PKCS7_decode("YELLOW SUBMARINE\x05\x05\x05\x05"))
except Exception, e:
	print(str(e))
'''
