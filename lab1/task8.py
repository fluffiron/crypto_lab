
def split_nth_chars(string, size_block):
	return [string[i:i + size_block] for i in range(0, len(string), size_block)]


def is_repeat_present(ct):
	ct_blocks = split_nth_chars(ct,16)
	if len(set(ct_blocks)) != len(ct_blocks):
		return True
	return False



with open("detectEcb.txt") as f:
	inp_lines = [s.rstrip()  for s in f.readlines()]

for item in inp_lines:
	if is_repeat_present(item.decode("hex")):
		print item
