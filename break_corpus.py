# -*- coding: utf-8 -*-

from lm_common import *
import codecs
import sys
import glob
import os.path

out_path = '/home/qiao/cse517_a1/wiki_dataset/train_test_holdout/'

for f in glob.glob('/home/qiao/cse517_a1/wiki_dataset/txt_output/*.txt'):
	text_name = os.path.basename(f).split(".txt")[0]
	print text_name
	raw_text = codecs.open(f, encoding='utf-8', mode='r').read()
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

        # add start symbol and end symbol
        train_set = START + START + train_set + EOT
	# no start symbols to test/holdout sets
        test_set = test_set + EOT
        holdout_set = holdout_set + EOT

	train_set_outfile = codecs.getwriter('utf-8')(file(out_path + text_name + '.train.txt', 'w'))
	train_set_outfile.write(train_set)
	train_set_outfile.flush()

	test_set_outfile = codecs.getwriter('utf-8')(file(out_path + text_name + '.test.txt', 'w'))
	test_set_outfile.write(test_set)
	test_set_outfile.flush()

	holdout_set_outfile = codecs.getwriter('utf-8')(file(out_path + text_name + '.holdout.txt', 'w'))
	holdout_set_outfile.write(holdout_set)
	holdout_set_outfile.flush()
