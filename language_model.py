# -*- coding: utf-8 -*-

# TODO
# Done read/process unicode
# Done smoothing/interpolation
# NO - data structures for cond prob
# No - trigram or more?
# Done - UNKOWN words, valid unicode but not BMP
# perplexity, tuning framework
# get all unicode corpus so all unigram is non-zero
# add two start symbols

from lm_common import *
import codecs
import sys
import random
import cPickle as pickle
import math

def append_to_history_clear_if_stop_symbol(history, c):
	# append to history
	# clear history if stop symbol
	history.append(c)
	if len(history) > 3:
		history.pop(0)
	if c == u'0003':
		# start with two start symbols
		history = [START, START]

def compute_ngram_logp(n, history, c):
	global total_unigram_counts
	global vocab_size
	global smooth_k1
	if n == 1:
		counts_c = 0
		if c in counts:
			counts_c = counts[c]
		return log(counts_c + smooth_k1) - log(total_unigram_counts + smooth_k1 * vocab_size)
	elif n <= 3:
		h_str = ''.join(history[-(n-1) : ])
		hv_str = h_str + c
		counts_h = 0
		counts_hv = 0
		if h_str in counts:
			counts_h = counts[h_str]
		if hv_str in counts:
			counts_hv = counts[hv_str]
		if n == 2:
			return log(counts_hv + smooth_k2) - log(counts_h + smooth_k2 * vocab_size)
		else:
			return log(counts_hv + smooth_k3) - log(counts_h + smooth_k3 * vocab_size)
	print 'not supported'
	exit(1)

def compute_cond_logp(history, c):
	logq1 = compute_ngram_logp(1, history, c)
	logq2 = compute_ngram_logp(2, history, c)
	logq3 = compute_ngram_logp(3, history, c)

	# if (len(history) == 0):
	# 	# print history
	# 	return logq1
	# elif (len(history) == 1):
	# 	# print history
	# 	logqmax = max(logq1, logq2)
	# 	assert (logq1 is not None)
	# 	assert (logq2 is not None)
	# 	t = l21 * math.pow(2, logq1 - logqmax)
	# 	t += l22 * math.pow(2, logq2 - logqmax)
	# 	logp = logqmax + log(t)
	# 	return logp
	# else:
	assert len(history) >= 2
	# print history
	logqmax = max(logq1, logq2, logq3)
	# print logq1, logq2, logq3
	assert (logq1 is not None)
	assert (logq2 is not None)
	assert (logq3 is not None)
	t = l31 * math.pow(2, logq1 - logqmax)
	t += l32 * math.pow(2, logq2 - logqmax)
	t += l33 * math.pow(2, logq3 - logqmax)
	logp = logqmax + log(t)
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
			return c
			# pass
	# 	logps += [(logp, ord_c, c)]
	# for x in sorted(logps, reverse=True)[0:30]:
	# 	print x
	return u'\uffff'

# set random seed
print 'get seed = ' + sys.argv[1]
random.seed(int(sys.argv[1]))

# set input, output to utf8
sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# load language model
word_count_filename = 'austen-emma.txt.total_unigram_counts_887074.counts'
# word_count_filename = 'test.txt.total_unigram_counts_29.counts'
counts = pickle.load(open(word_count_filename, "rb"))

# vocab size
total_unigram_counts = int(word_count_filename.split('.')[-2].split('_')[-1])
# print 'total_unigram_counts = ' + str(total_unigram_counts)


##################################

# # compute perplexity
# texts = [\
# u'abcdefghijklmnopqrstuvwxyz\u0003',\
# ]

# N_words = 0

# logp_sum = 0
# for text in texts:
# 	logp_sum_per_text = 0
# 	history = []
# 	for c in text:
# 		N_words += 1
# 		logp = compute_cond_logp(history, c)
# 		logp_sum_per_text += logp
# 		append_to_history_clear_if_stop_symbol(history, c)
# 	logp_sum += logp_sum_per_text
# perplexity = math.pow(2, -1.0 * logp_sum / N_words)
# print 'perplexity = %f' % perplexity

##################################

# user interaction
history = [START, START]
while True:
	cmd = sys.stdin.read(size=1, chars=1)
	print cmd, history
	if cmd == u'o':
		# observe next char c
		c = convert_to_UNK(sys.stdin.read(size=1, chars=1))
		print u'observe char ' + c
		append_to_history_clear_if_stop_symbol(history, c)
	elif cmd == u'q':
		c = convert_to_UNK(sys.stdin.read(size=1, chars=1))
		print u'print prob for char ' + c
		logp = compute_cond_logp(history, c)
		print logp
	elif cmd == u'g':
		c = generate_char(history)
		print u'randomly generate char ' + c
		append_to_history_clear_if_stop_symbol(history, c)
	elif cmd == u'x':
		print u'quit'
		break
	else:
		print u'ERROR in parsing command'
		exit(1)
