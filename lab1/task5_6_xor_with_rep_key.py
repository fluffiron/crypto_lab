import operator
import math
import string

def is_ascii(s):
	forbidden = set("%^{}[]^+=#`")
	is_forbidden = bool(set(s).intersection(forbidden))
	return all(c in string.printable for c in s) and (not is_forbidden )
def english_detect(open_text_dict):
	if type(open_text_dict) != dict :
		return ""
	arr = [ 8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074 ]

	open_text_dict = {key : text  for key, text in open_text_dict.items() if is_ascii(text)}

	if len(open_text_dict) == 0:
		return ""
	inv_prob = {}
	for key,text in open_text_dict.items():
		text = text.upper()
		deltas = [ text.count( chr(i) ) / float( len( text) - text.count(" ") )	for i in range( ord("A"), ord("Z") + 1 )]
		prob = 0
		for i in range( len(arr) ):
			prob += deltas[i] - arr[i]
		inv_prob[key] = prob

	min_key = min(inv_prob.iteritems(), key=operator.itemgetter(1))[0]	

#	print(open_text_dict[min_key])	

	return chr(min_key)
		

def decrypt_by_one_char(in_lst, char):
	if type(char) == int and isinstance(in_lst, list):
#		ar_bytes=[in_str[i:i+2] for i in range(0,len(in_str), 2)]
		
		return ''.join([chr(int(i, 16) ^ char) for i in in_lst])
	else:
		return ""

def XOR(lst_in, key):
	long_key = ""
	if len(key) != 0:
		for i in range( len(lst_in) / len(key) ):
			long_key += key
		long_key += key[: len(lst_in) % len(key)] 
	
		return "".join( chr( int(a, 16) ^ ord(b) ) for a,b in zip(lst_in, long_key))
	else:
		return "keyzero"


filename="breakRepeatedKeyXor.txt"

with open(filename) as f:
	content = f.readlines()
input_string = ""
for x in content:
	input_string += x.strip()
# translate input string into hex
input_string = input_string.decode("base64").encode("hex")

#split input string
ar_bytes=[input_string[i:i+2] for i in range(0,len(input_string), 2)] 


for k_len in range(2,41):
	buff = [ [] for i in range(k_len) ]
	for i in range( len(ar_bytes) ):
		buff[ i % k_len ].append(ar_bytes[i])
	key = ""

	for lst_sub in buff:
		d_tmp ={}
		for i in range(30, 128):
			d_tmp[i] = decrypt_by_one_char(lst_sub,i)
		key += english_detect(d_tmp)
	print("key= " + key)
	print(XOR(ar_bytes,key))

'''
	possible_keys = []
	for lst_sub in buff:
		pos_k=[]
		for i in range(256):
			tmp_text = decrypt_by_one_char(lst_sub,i)
			if is_ascii(tmp_text):
				pos_k.append(i)
		possible_keys.append(pos_k)
	

	sumi=1
	for i in possible_keys:
		sumi *= len(i)
	print(str(k_len) + " " +str(sumi))

				

		tmp = english_detect(res_dict)
		if len(tmp) == 0:
			Error = True
	if Error :
		print(str(k_len) + "is not possible")	
#	out_line = XOR(ar_bytes, key)
#	print("key= " + key)
	tmp_str = XOR(ar_bytes,key)
	print("open= " + tmp_str)
'''

