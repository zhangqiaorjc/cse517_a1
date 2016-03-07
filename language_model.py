# -*- coding: utf-8 -*-

# TODO
# Done read/process unicode
# Done smoothing/interpolation
# NO - data structures for cond prob
# Yes - trigram or more? 4grams
# Done - UNKOWN words, valid unicode but not BMP
# Yes perplexity, tuning framework
# get all unicode corpus so all unigram is non-zero
# DONE add two start symbols

from lm_common import *
import codecs
import sys
import random
import cPickle as pickle
import math
import os

def append_to_history_clear_if_stop_symbol(history, c):
	# append to history
	# clear history if stop symbol
	history.append(c)
	if len(history) > 4:
		history.pop(0)
	if c == EOT:
		# start with three start symbols
		history = [START, START, START]

def compute_ngram_logp(n, history, c):
	global total_unigramCounts
	global vocab_size
	global smooth_k1
	global smooth_k2
	global smooth_k3
	global smooth_k4
	if n == 1:
		counts_c = 0
		if c in unigramCounts:
			counts_c = unigramCounts[c]
		return log(counts_c + smooth_k1) - log(total_unigramCounts + smooth_k1 * vocab_size)
	elif n == 2:
		h_str = ''.join(history[-(n-1) : ])
		hv_str = h_str + c
		counts_h = 0
		counts_hv = 0
		if h_str in unigramCounts:
			counts_h = unigramCounts[h_str]
		if hv_str in bigramCounts:
			counts_hv = bigramCounts[hv_str]
		return log(counts_hv + smooth_k2) - log(counts_h + smooth_k2 * vocab_size)
	elif n == 3:
		h_str = ''.join(history[-(n-1) : ])
		hv_str = h_str + c
		counts_h = 0
		counts_hv = 0
		if h_str in bigramCounts:
			counts_h = bigramCounts[h_str]
		if hv_str in trigramCounts:
			counts_hv = trigramCounts[hv_str]
		return log(counts_hv + smooth_k3) - log(counts_h + smooth_k3 * vocab_size)
	elif n == 4:
		h_str = ''.join(history[-(n-1) : ])
		hv_str = h_str + c
		counts_h = 0
		counts_hv = 0
		if h_str in trigramCounts:
			counts_h = trigramCounts[h_str]
		if hv_str in quadgramCounts:
			counts_hv = quadgramCounts[hv_str]
		return log(counts_hv + smooth_k4) - log(counts_h + smooth_k4 * vocab_size)
	print 'not supported'
	sys.exit(1)

def compute_cond_logp(history, c):
	logq1 = compute_ngram_logp(1, history, c)
	logq2 = compute_ngram_logp(2, history, c)
	logq3 = compute_ngram_logp(3, history, c)
	logq4 = compute_ngram_logp(4, history, c)
	assert len(history) >= 3
	# print history
	logqmax = max(logq1, logq2, logq3, logq4)
	# print logq1, logq2, logq3
	assert (logq1 is not None)
	assert (logq2 is not None)
	assert (logq3 is not None)
	assert (logq4 is not None)
	t = l41 * math.pow(2, logq1 - logqmax)
	t += l42 * math.pow(2, logq2 - logqmax)
	t += l43 * math.pow(2, logq3 - logqmax)
	t += l44 * math.pow(2, logq4 - logqmax)
        try:
            logp = logqmax + log(t)
        except Exception, e:
            print logq1, logq2, logq3, logq4, t
	return logp

def compute_logsum(logp_list):
	logp_max = max(logp_list)
	t = 0
	for logp in logp_list:
		if logp is not None:
			t += math.pow(2, logp - logp_max)
	logpsum = logp_max + log(t)
	return logpsum 

def generate_char(history):
	logr = log(random.random())
	logps = []
	# print 'logr = %f' % logr
	logsum = None
	for ord_c in xrange(0, 0xffff + 1):
		# print ord_c
		if ((ord_c >= 0x0860 and ord_c <= 0x089F) \
			or (ord_c >= 0x1c80 and ord_c <= 0x1cbf) \
			or (ord_c >= 0x2fe0 and ord_c <= 0x2fef)):
			continue
		c = unichr(ord_c)
		logp = compute_cond_logp(history, c)
		logsum = compute_logsum([logsum, logp])
		# print 'logsum = %f' % logsum
		if logsum > logr:
			return c, logp
			# pass
	# print 'logsum=%f' % logsum
	# 	logps += [(logp, ord_c, c)]
	# for x in sorted(logps, reverse=True)[0:30]:
	# 	print x
	return u'\uffff', 0.0

# set random seed
# print 'get seed = ' + sys.argv[1]
random.seed(int(sys.argv[1]))

# set input, output to utf8
sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# load language model
unigram_filename = 'all.unigram'
bigram_filename = 'all.bigram'
trigram_filename = 'all.trigram'
quadgram_filename = 'all.quadgram'

unigramCounts = pickle.load(open(unigram_filename, "rb"))
assert len(unigramCounts) > 0
bigramCounts = pickle.load(open(bigram_filename, "rb"))
assert len(bigramCounts) > 0
trigramCounts = pickle.load(open(trigram_filename, "rb"))
assert len(trigramCounts) > 0
quadgramCounts = pickle.load(open(quadgram_filename, "rb"))
assert len(quadgramCounts) > 0

# vocab size
#total_unigramCounts = int(unigram_filename.split('.')[-2].split('_')[-1])
#print 'total_unigramCounts = ' + str(total_unigramCounts)

total_unigramCounts = 0
for k in unigramCounts:
    total_unigramCounts += unigramCounts[k]
# print 'found count = ' + str(total_unigramCounts)

##################################

# compute perplexity
# expect the texts are separated by EOT, otherwise will hang

if False:
  holdout_texts = sys.stdin.read()
  texts = holdout_texts.split(EOT)
  print "%d holdout texts" % len(texts)

  M_words = 0
  logp_sum = 0
  for text in texts:
    if len(text) == 0: continue
    text += EOT
    history = [START, START, START]
    for c in text:
      c = convert_to_UNK(c)
      if c != EOT:
        M_words += 1
        logp = compute_cond_logp(history, c)
        logp_sum += logp
      append_to_history_clear_if_stop_symbol(history, c)
  perplexity = -1.0 * logp_sum / M_words
  print 'perplexity = %f' % perplexity
  exit(0)

def compute_perplexity(raw_text):
    logp_sum = 0.0
    history = [START, START, START]
    for c in raw_text + EOT:
        c = convert_to_UNK(c)
        logp_sum += compute_cond_logp(history, c)
        append_to_history_clear_if_stop_symbol(history, c)
    return len(raw_text) + 1, logp_sum

def compute_perplexity_for(z):
    k1, k2, k3, k4, l1, l2, l3 = z
    holdout_data_dir = './language_data/'
    global smooth_k1, smooth_k2, smooth_k3, smooth_k4
    global l41, l42, l43, l44
    smooth_k1 = k1
    smooth_k2 = k2
    smooth_k3 = k3
    smooth_k4 = k4
    l41 = l1
    l42 = l2
    l43 = l3
    l44 = 1.0 - l41 - l42 - l43
    total_nchars = 0
    total_logprob = 0.0
    total_perplexity = 0.0
    for root, dirs, files in os.walk(holdout_data_dir):
        for fname in files:
            f = os.path.join(root, fname)
            raw_text = codecs.open(f, encoding='utf-8', mode='r').read()
            nchars, logprob = compute_perplexity(raw_text)
            total_nchars += nchars
            total_logprob += logprob
    if total_nchars == 0:
        print 'zero chars'
    total_perplexity = math.pow(2, -1.0 * total_logprob / total_nchars)
    return total_perplexity

#print 'computing'
#print compute_perplexity_for((1e-7, 1e-7, 1e-7, 1e-7, 0.001, 0.01, 0.1)) 

def grid_search_for_parameters(fname):
    import cPickle as pickle
    count = 0
    results = {}
    for k1 in [1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        for k2 in [1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
            for k3 in [1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
                for k4 in [1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
                    for l1 in [5e-1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
                        for l2 in [5e-1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
                            z = (k1, k2, k3, l1, l2) 
                            perp = compute_perplexity_for(z)
                            print z, perp
                            results[perp] = z
                            count += 1
                            if (count % 100 == 0):
                                pickle.dump(results, open(fname, 'wb'))
    import operator
    sorted_results = sorted(results.items(), key=operator.itemgetter(0))
    for item in sorted_results:
        print item

    pickle.dump(sorted_results, open(fname, 'wb'))

# grid_search_for_parameters('gridsearch.dict')

##################################

# user interaction
history = [START, START, START]
while True:
	cmd = sys.stdin.read(size=1, chars=1)
	# print cmd, history
	if cmd == u'o':
		c = convert_to_UNK(sys.stdin.read(size=1, chars=1))
		print u'// observed a char '
		append_to_history_clear_if_stop_symbol(history, c)
	elif cmd == u'q':
		c = convert_to_UNK(sys.stdin.read(size=1, chars=1))
		logp = compute_cond_logp(history, c)
		print logp
	elif cmd == u'g':
		c, logp = generate_char(history)
		print c + "//" + str(logp)
		append_to_history_clear_if_stop_symbol(history, c)
	elif cmd == u'x':
		break
	else:
		print u'ERROR in parsing command'
		sys.exit(1)
