from lm_common import *
import codecs
import sys

import os.path
import cPickle as pickle
import glob

indir = sys.argv[1]

quadgramCounts = {}
quadgramName = 'all.quadgram'

print 'combine quadgrams'
for f in glob.glob(os.path.join(indir, '*.quadgram')):
        print f
	ngram = pickle.load(open(f, 'rb'))
	for k in ngram:
	    if k not in quadgramCounts:
		quadgramCounts[k] = 0
	    quadgramCounts[k] += ngram[k]

print "save to " + quadgramName
pickle.dump(quadgramCounts, open(quadgramName, "wb"))

