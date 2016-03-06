from lm_common import *
import codecs
import sys

import os.path
import cPickle as pickle

#reader = codecs.getreader('utf8')(sys.stdin)

filename = sys.argv[1]
outdir = sys.argv[2]

basename = os.path.basename(filename)
unigramName = os.path.join(outdir, basename + '.unigram')
bigramName = os.path.join(outdir, basename + '.bigram')
trigramName = os.path.join(outdir, basename + '.trigram')

print unigramName
print bigramName
print trigramName
if os.path.exists(unigramName) and os.path.exists(bigramName) and os.path.exists(trigramName):
    print "word count done already"
    sys.exit(0)

f = open(filename, 'rb')
reader = codecs.getreader('utf8')(f)

unigramCounts = {}
bigramCounts = {}
trigramCounts = {}

def update_counts(snippet):
	snippet = convert_to_UNK(snippet)
	# print snippet
	for i in xrange(1, len(snippet) + 1):
		ngram = snippet[0:i]
		# print ngram
		if i == 1:
		    # unigram
		    if ngram not in unigramCounts:
			    unigramCounts[ngram] = 0
		    unigramCounts[ngram] += 1
		elif i == 2:
		    # bigram
		    if ngram not in bigramCounts:
			    bigramCounts[ngram] = 0
		    bigramCounts[ngram] += 1
		elif i == 3:
		    # trigram
		    if ngram not in trigramCounts:
			    trigramCounts[ngram] = 0
		    trigramCounts[ngram] += 1
		else:
		    print ngram
		    print 'i = %d' % i
		    sys.exit(1)

# use trigram
buf = START + START
#total_unigram_counts = 2
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
	while idx + 3 < len(buf):
		snippet = buf[idx: idx + 3]
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

print "save to " + unigramName
pickle.dump(unigramCounts, open(unigramName, "wb"))

print "save to " + bigramName
pickle.dump(bigramCounts, open(bigramName, "wb"))

print "save to " + trigramName
pickle.dump(trigramCounts, open(trigramName, "wb"))

# print unigramCounts
# print bigramCounts
# print trigramCounts
