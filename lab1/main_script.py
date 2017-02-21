
base64_alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def XOR_buf(buf1, buf2):
	res=int(buf1,16) ^ int(buf2,16)
	return format(res, 'x')

def hex_to_base64(hex_str):
	if len(hex_str) % 2 == 1:
		return "Bad format"
	try:
		int(hex_str, 16)
	except:
		return "Bad format"
	acsii_str = "".join( chr(int(hex_str[i:i+2],16)) for i in range(0, len(hex_str), 2))
	encode_string = ""
# left variable remembers that left shift required
	left = 0
	for i in range(len(acsii_str)):
		if left == 0:
# ascii symbol has got 8 bit but we need only 6 thus shift to the right 2 times
			encode_string += base64_alp[ord(acsii_str[i]) >> 2]
# 2 shift to the left is required next time
			left = 2
		else:
			if left == 6:

				encode_string += base64_alp[ord(acsii_str[i - 1]) & 63]
				encode_string += base64_alp[ord	(acsii_str[i]) >> 2 ]
				left = 2
			else:
				index1 = ord(acsii_str[i - 1]) & (2 ** left - 1)
				index2 = ord(acsii_str[i]) >> (left + 2)
				index = (index1 << (6 - left)) | index2
				encode_string += base64_alp[index]
				left += 2
	if left != 0:
		encode_string += base64_alp[(ord(acsii_str[len(acsii_str) - 1]) & (2 ** left - 1)) << (6 - left)]
	encode_string += "=" * ((4 - len(encode_string) % 4) % 4)
	return encode_string
#	return hex_str.decode("hex").encode("base64")

def base64_to_hex(base64_str):
	decode_string = ""
	if base64_str.count("=") != ( 4 - (len(base64_str) - base64_str.count("=")) % 4 ) % 4:
		return "Bad format"
#	print(base64_str)
	base64_str = base64_str.replace("=", "")
	left = 0
	for i in range(len(base64_str)):
		if left == 0:
			left = 6
		else:
			value1 = base64_alp.index(base64_str[i - 1]) & (2 ** left - 1)
			value2 = base64_alp.index(base64_str[i]) >> (left - 2)
			value = (value1 << (8 - left)) | value2
			decode_string += chr(value)
			left -= 2
	return "".join(["{:02x}".format(ord(char)) for char in decode_string])

#	return base64_str.decode("base64").encode("hex")

inp= raw_input()
b64 =  hex_to_base64(inp)
print(b64)
print(base64_to_hex(raw_input()))

a="8f29336f5e9af0919634f474d248addaf89f6e1f533752f52de2dae0ec3185f818c0892fdc873a69"
b="bf7962a3c4e6313b134229e31c0219767ff59b88584a303010ab83650a3b1763e5b314c2f1e2f166"

print(XOR_buf(a,b))
