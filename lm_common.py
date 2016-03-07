import math

# end of text symbol
EOT = u'\u0003'

# START symbol
START = u'\u0858'

# UNKNOWN symbol
UNK = u'\u0859'

# k for additive smoothing
smooth_k1 = 0.0000001
smooth_k2 = 0.0000001
smooth_k3 = 0.0000001
smooth_k4 = 0.0000001
vocab_size = 65392

def convert_to_UNK(snippet):
	converted_snippet = list(snippet)
	for i in xrange(len(snippet)):
		ord_c = ord(snippet[i])
		if (ord_c > 0xffff or (ord_c >= 0x0860 and ord_c <= 0x089F) \
						   or (ord_c >= 0x1c80 and ord_c <= 0x1cbf) \
						   or (ord_c >= 0x2fe0 and ord_c <= 0x2fef)):
			converted_snippet[i] = UNK
	converted_snippet = ''.join(converted_snippet)
	return converted_snippet

# interpolation parameters
l41 = 0.001
l42 = 0.01
l43 = 0.1
l44 = 1.0 - l41 - l42 - l43

# use log base 2 throughout
def log(x):
	return math.log(x, 2)
