from lm_common import *
import codecs
import sys

import os.path
import cPickle as pickle
import glob

indir = sys.argv[1]

unigramCounts = {}
bigramCounts = {}
trigramCounts = {}

print 'combine unigrams'
for f in glob.glob(os.path.join(indir, '*.unigram')):
	ngram = pickle.load(open(f, 'rb'))
	for k in ngram:
	    if k not in unigramCounts:
		unigramCounts[k] = 0
	    unigramCounts[k] += ngram[k]

print 'combine bigrams'
for f in glob.glob(os.path.join(indir, '*.bigram')):
	ngram = pickle.load(open(f, 'rb'))
	for k in ngram:
	    if k not in bigramCounts:
		bigramCounts[k] = 0
	    bigramCounts[k] += ngram[k]

print 'combine trigrams'
for f in glob.glob(os.path.join(indir, '*.trigram')):
	ngram = pickle.load(open(f, 'rb'))
	for k in ngram:
	    if k not in trigramCounts:
		trigramCounts[k] = 0
	    trigramCounts[k] += ngram[k]

unigramName = 'all.unigram'
bigramName = 'all.bigram'
trigramName = 'all.trigram'

print "save to " + unigramName
pickle.dump(unigramCounts, open(unigramName, "wb"))

print "save to " + bigramName
pickle.dump(bigramCounts, open(bigramName, "wb"))

print "save to " + trigramName
pickle.dump(trigramCounts, open(trigramName, "wb"))

