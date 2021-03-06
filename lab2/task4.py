import operator
import math
import string

def is_ascii(s):
	return all( ord(c) > 128 for c in s)
#	return all(c in string.printable for c in s)

def english_detect(open_text_dict):
	if type(open_text_dict) != dict :
		return ""
	arr = [ 8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074 ]

	open_text_dict = {key : text  for key, text in open_text_dict.items() if is_ascii(text)}

	if len(open_text_dict) == 0:
		print "There is no ascii string!"
		return ""
	inv_prob = {}
	for key,text in open_text_dict.items():
		text = text.upper()
		deltas = [ text.count( chr(i) ) / float( len( text) )	for i in range( ord("A"), ord("Z") + 1 )]
		prob = 0
		for i in range( len(arr) ):
			prob += deltas[i] - arr[i]
		inv_prob[key] = prob

	min_key = min(inv_prob.iteritems(), key=operator.itemgetter(1))[0]	
	print "not zero"
	return chr(min_key)

def decrypt_by_one_char(in_str, char):
	return ''.join([chr(ord(i) ^ char) for i in in_str])

def XOR(str_in, key):
	long_key = ""
	if len(key) != 0:
		for i in range( len(str_in) / len(key) ):
			long_key += key
		long_key += key[: len(str_in) % len(key)] 
	
		return "".join( chr( ord(a) ^ ord(b) ) for a,b in zip(str_in, long_key))
	else:
		return "keyzero"


encrypted_lines_b64 = open("Lab2_breakctr3-b64.txt")
encrypted_lines = [i.decode("base64") for i in encrypted_lines_b64]

min_string_len = min( map(len, encrypted_lines) )


encrypted_lines = [i[:min_string_len] for i in encrypted_lines]


xor_enc_lines = []
for i in range( min_string_len ):
	tmp_xor_line = ""
	for input_line in encrypted_lines:
		tmp_xor_line += input_line[i]
	xor_enc_lines.append(tmp_xor_line)

key = ""

for line in xor_enc_lines:
#	print line
	d_tmp ={}
	for i in range(256):
		d_tmp[i] = decrypt_by_one_char(line,i)
	tmp = english_detect(d_tmp)
#	print tmp
	key += tmp

print XOR(encrypted_lines[0],key)



