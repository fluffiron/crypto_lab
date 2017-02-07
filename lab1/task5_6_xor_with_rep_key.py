
def XOR(str_in, key):
	if isinstance(str_in, str)  == False and isinstance(key, str) == False:
		return ""
	long_key = ""
	for i in range( len(str_in) / len(key) ):
		long_key += key
	long_key += key[: len(str_in) % len(key)] 
	
	return "".join('{:02x}'.format(ord(a) ^ ord(b)) for a,b in zip(str_in, long_key))

s = "NNNNN"
key = "ICE"
print(XOR(s,key))
