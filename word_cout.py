from lm_common import *
import codecs
import sys
import cPickle as pickle

reader = codecs.getreader('utf8')(sys.stdin)

counts = {}

def update_counts(snippet):
	snippet = convert_to_UNK(snippet)
	# print snippet
	for i in xrange(1, len(snippet) + 1):
		ngram = snippet[0:i]
		# print ngram
		if ngram not in counts:
			counts[ngram] = 0
		counts[ngram] += 1

snippet = u''
idx = 0
# use trigram
buf = START + START
total_unigram_counts = 2

while True:
	buf = buf[idx:] 
	new_text = reader.read()
	if len(new_text) == 0:
		# end of input
		break
	total_unigram_counts += len(new_text)
	buf = buf + new_text
	idx = 0
	while idx + 3 < len(buf):
		snippet = buf[idx: idx + 3]
		update_counts(snippet)
		idx += 1

# append end of text character
buf = buf + EOT
total_unigram_counts += 1
for i in xrange(len(buf)):
	update_counts(buf[i:])

# save counts
print counts
filename = sys.argv[1] + '.total_unigram_counts_' + str(total_unigram_counts) + '.counts'
print "save to " + filename
pickle.dump(counts, open(filename, "wb"))