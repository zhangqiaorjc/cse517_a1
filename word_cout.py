from lm_common import *
import codecs
import sys
import cPickle as pickle

reader = codecs.getreader('utf8')(sys.stdin)

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
		    print 'i = %d' %d
		    sys.exit(1)

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
#buf = buf + EOT
#total_unigram_counts += 1
for i in xrange(len(buf)):
	update_counts(buf[i:])

unigramName = sys.argv[1] + '.total_unigram_counts_' + str(total_unigram_counts) + '.unigram'
print "save to " + unigramName
pickle.dump(unigramCounts, open(unigramName, "wb"))

bigramName = sys.argv[1] + '.total_unigram_counts_' + str(total_unigram_counts) + '.bigram'
print "save to " + bigramName
pickle.dump(bigramCounts, open(bigramName, "wb"))

trigramName = sys.argv[1] + '.total_unigram_counts_' + str(total_unigram_counts) + '.trigram'
print "save to " + trigramName
pickle.dump(trigramCounts, open(trigramName, "wb"))

# print unigramCounts
# print bigramCounts
# print trigramCounts
