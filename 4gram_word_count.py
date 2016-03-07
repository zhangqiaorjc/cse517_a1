from lm_common import *
import codecs
import sys

import os.path
import cPickle as pickle

#reader = codecs.getreader('utf8')(sys.stdin)

filename = sys.argv[1]
outdir = sys.argv[2]

basename = os.path.basename(filename)
quadgramName = os.path.join(outdir, basename + '.quadgram')

print quadgramName
if os.path.exists(quadgramName):
    print "word count done already"
    sys.exit(0)

f = open(filename, 'rb')
reader = codecs.getreader('utf8')(f)

quadgramCounts = {}

def update_counts(snippet):
	snippet = convert_to_UNK(snippet)
	# print snippet
	for i in xrange(4, len(snippet) + 1):
		ngram = snippet[0:i]
		# print ngram
		if i == 4:
		    # quadgram
		    if ngram not in quadgramCounts:
			    quadgramCounts[ngram] = 0
		    quadgramCounts[ngram] += 1
		else:
		    print ngram
		    print 'i = %d' % i
		    sys.exit(1)

# use quadgram
buf = START + START + START
terminate = False
while True:
	new_text = reader.read()
	if len(new_text) == 0:
		# append end of text character
		new_text = EOT
		terminate = True
	#total_unigram_counts += len(new_text)
	buf = buf + new_text
	idx = 0
	while idx + 4 < len(buf):
		snippet = buf[idx: idx + 4]
		update_counts(snippet)
		idx += 1
	buf = buf[idx:] 
	if terminate:
	    # end of input
	    break

# buf = buf + EOT
#total_unigram_counts += 1
for i in xrange(len(buf)):
	update_counts(buf[i:])

print "save to " + quadgramName
pickle.dump(quadgramCounts, open(quadgramName, "wb"))
