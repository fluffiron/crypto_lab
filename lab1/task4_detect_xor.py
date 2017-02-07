import operator
import math

def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def english_detect(open_text_dict):
	if type(open_text_dict) != dict :
		return {}
	arr = [ 8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074 ]

	open_text_dict = {key : text  for key, text in open_text_dict.items() if is_ascii(text)}

	inv_prob = {}
	for key,text in open_text_dict.items():
		text = text.upper()
		deltas = [ text.count( chr(i) ) / float( len( text) - text.count(" "))	for i in range( ord("A"), ord("Z") + 1 )]
		prob = 0
		for i in range( len(arr) ):
			prob += ( deltas[i] - arr[i] ) ** 2
		inv_prob[key] = math.sqrt(prob)
	if len(inv_prob) == 0:
		return {}
	min_key = min(inv_prob.iteritems(), key=operator.itemgetter(1))[0]	

#	print(open_text_dict)	

	return {min_key : open_text_dict[ min_key ] }
		

def decrypt_by_one_char(in_str, char):
	if type(char) == int and isinstance(in_str, str):
		ar_bytes=[in_str[i:i+2] for i in range(0,len(in_str), 2)]
		
		return ''.join([chr(int(i, 16) ^ char) for i in ar_bytes])
	else:
		return ""
filename="detectSingleXor05"

with open(filename) as f:
	content = f.readlines()
content = [x.strip() for x in content]

for cipher in content:
	res_dict={}
	for i in range(256):
		res_dict[i] = decrypt_by_one_char(cipher,i)
#print(res_dict)
	for key, text in english_detect(res_dict).items():
		print(chr(key) + ":   " + text)
	
