
def decrypt_by_one_char(in_str, char):
	if type(char) == int and isinstance(in_str, str):
		ar_bytes=[in_str[i:i+2] for i in range(0,len(in_str), 2)]
		
		return ''.join([chr(int(i, 16) ^ char) for i in ar_bytes])
	else:
		return ""
date="191f1911160b0c580c101d581d0e1114583f1914191b0c111b583d1508110a1d56"		
for i in range(64,123):
	print(decrypt_by_one_char(date,i))

