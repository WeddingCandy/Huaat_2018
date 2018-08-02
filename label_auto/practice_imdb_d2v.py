"""@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
"""

import gensim

LabeledSentence = gensim.models.doc2vec.LabeledSentence
from sklearn.model_selection import train_test_split
import numpy as np
with open('IMDB_data/pos.txt','r') as infile:
    pos_reviews = infile.readlines()

with open('IMDB_data/neg.txt','r') as infile:
    neg_reviews = infile.readlines()

with open('IMDB_data/unsup.txt','r') as infile:
    unsup_reviews = infile.readlines()

