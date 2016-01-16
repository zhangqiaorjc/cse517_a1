# -*- coding: utf-8 -*-

import codecs
import sys

from nltk.corpus import gutenberg

# writer = codecs.getwriter('utf8')(sys.stdout)

# emma = gutenberg.raw('austen-emma.txt').replace("\n", " ")

# writer.write(emma)

for f in gutenberg.fileids():
	text_name = '/Users/qiao/repos/cse517_a1/datasets/' + f.split(".txt")[0]
	print text_name
	raw_text = gutenberg.raw(f)
	text_len = len(raw_text)
	train_set_len = int(text_len * 0.8)
	test_set_len = int(text_len * 0.1)
	holdout_set_len = text_len - train_set_len - test_set_len
	print train_set_len, test_set_len, holdout_set_len

	last = 0
	train_set = raw_text[0 : train_set_len]
	last += train_set_len
	test_set = raw_text[last : last + test_set_len]
	last += test_set_len
	holdout_set = raw_text[last : last + holdout_set_len]
	last += holdout_set_len

	assert (last == text_len)

	train_set_outfile = codecs.getwriter('utf-8')(file(text_name + '.train.txt', 'w'))
	train_set_outfile.write(train_set)
	train_set_outfile.flush()

	test_set_outfile = codecs.getwriter('utf-8')(file(text_name + '.test.txt', 'w'))
	test_set_outfile.write(test_set)
	test_set_outfile.flush()

	holdout_set_outfile = codecs.getwriter('utf-8')(file(text_name + '.holdout.txt', 'w'))
	holdout_set_outfile.write(holdout_set)
	holdout_set_outfile.flush()

	# close(train_set_outfile)
	# close(test_set_outfile)
	# close(holdout_set_outfile)