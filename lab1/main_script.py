
def XOR_buf(buf1, buf2):
	res=int(buf1,16) ^ int(buf2,16)
	return format(res, 'x')

def hex_to_base64(hex_str):
	return hex_str.decode("hex").encode("base64")

def base64_to_hex(base64_str):
	return base64_str.decode("base64").encode("hex")

b64 =  hex_to_base64("faea8766efd8b295a633908a3c0828b22640e1e9122c3c9cfb7b59b7cf3c9d448bf04d72cde3aaa0")
print(b64)
print(base64_to_hex(b64))

a="8f29336f5e9af0919634f474d248addaf89f6e1f533752f52de2dae0ec3185f818c0892fdc873a69"
b="bf7962a3c4e6313b134229e31c0219767ff59b88584a303010ab83650a3b1763e5b314c2f1e2f166"

print(XOR_buf(a,b))
