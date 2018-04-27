#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
"""

from __future__ import division

import os
import sys
import time
import logging
import argparse
from tqdm import tqdm
from prettytable import PrettyTable

import numpy as np
from gensim.models.word2vec import Word2Vec
from sklearn.neighbors import NearestNeighbors

from data import (SEED, get_data)

logger = logging.getLogger(__name__)


def evaluation(train, test,
               size_embedding, window_size, min_count, workers, it, sample, neg_sample, power_alpha, k):
    """
    Split the raw sessions into training sessions for p2v and mp2v and a common test set.

        train: list
        List (of length nb_sessions) of lists of strings ['item_0', ..., 'item_(n-1)'].

        test: list
        List (of length nb_sessions) of lists of strings ['item_(n-1)','item_n'].

    """

    # Training modified Word2Vec model.
    t = time.time()
    model = Word2Vec(train, size=size_embedding,
                     window=window_size, min_count=min_count, workers=workers, sg=1, iter=it, sample=sample,
                     negative=neg_sample, power_alpha=power_alpha)
    print "took %1.2f minutes." % ((time.time()-t)/60.)

    # Create a matrix filled with embeddings of all items considered.
    if model.wv.vocab.keys()[0].startswith('track') or model.wv.vocab.keys()[0].startswith('artist'):
        track_elems = [_ for _ in model.wv.vocab.keys() if _.startswith('track')]
    else:
        track_elems = [_ for _ in model.wv.vocab.keys()]
    embedding = [model.wv[elem] for elem in track_elems]
    mapping = {elem: i for i, elem in enumerate(track_elems)}
    mapping_back = {v: k for k, v in mapping.items()}

    # Fit nearest neighbour model.
    neigh = NearestNeighbors()
    neigh.fit(embedding)

    hrk_score = 0.0
    ndcg_score = 0.0
    t = time.time()
    print "Computing scores..."
    for pair_items in tqdm(test):
        emb_0 = embedding[mapping[pair_items[0]]].reshape(1, -1)
        if str(pair_items[1]) == str(pair_items[0]):
             # HR@k
            hrk_score += 1/k
            # NDCG@k
            ndcg_score += 1
        else:
             # get neighbors
             emb_neighbors = neigh.kneighbors(emb_0, k+1)[1].flatten()[1:]
             neighbors = [mapping_back[x] for x in emb_neighbors]
             if str(pair_items[1]) in neighbors:
                 # HR@k
                 hrk_score += 1/k
                 # NDCG@k
                 # In our case only one item in the retrived list can be relevant,
                 # so in particular the ideal ndcg is 1 and ndcg_at_k = 1/log_2(1+j)
                 # where j is the position of the relevant item in the list.
                 index_match = (np.where(str(pair_items[1]) == np.array(neighbors)))[0][0]
                 ndcg_score += 1/np.log2(np.arange(2, k+2))[index_match]
    hrk_score = hrk_score / len(test)
    ndcg_score = ndcg_score / len(test)

    print "took %1.2f minutes." % ((time.time()-t)/60.)

    return {"k": k, "ndcg_score": ndcg_score, "hrk_score": hrk_score}

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger.info("running %s", " ".join(sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_data', dest='path_data', required=True, type=str)
    parser.add_argument('--p2v', help="Evaluate prod2vec", dest='p2v', default=True, type=bool)
    parser.add_argument('--size_embedding', dest='size_embedding', default=50, type=int)
    parser.add_argument('--window_size', dest='window_size', default=3, type=int)
    parser.add_argument('--min_count', dest='min_count', default=1, type=int)
    parser.add_argument('--workers', dest='workers', default=10, type=int)
    parser.add_argument('--it', dest='it', default=110, type=int)
    parser.add_argument('--sample', dest='sample', default=0.00001, type=float)
    parser.add_argument('--neg_sample', dest='neg_sample', default=5, type=int)
    parser.add_argument('--power_alpha', dest='power_alpha', default=-0.5, type=float)
    parser.add_argument("--it_conf", help="Number of iterations for confidence intervals", default=10, type=int)
    parser.add_argument('--k', dest='k', default=10, type=int)
    args = parser.parse_args()

    train_p2v, train_mp2v, validation, test = get_data(args.path_data)

    # Create table with results
    scores = {}
    t = PrettyTable(['Model', 'HR@10', 'NDCG@10'])
    name = os.path.split(args.path_data)[-1].split(".")[0]
    # Run to compute confidence interval
    for i in range(args.it_conf):
        if args.p2v:
            logger.info("Evaluating Word2Vec model...")
            results = evaluation(train_p2v, test,
                                 args.size_embedding, args.window_size, args.min_count, args.workers, args.it,
                                 args.sample, args.neg_sample, args.power_alpha, args.k)
            model_name = 'Prod2vec_{}_{}_{}_{}_{}_run_{}'.format(
                name,
                args.window_size,
                args.it,
                args.sample,
                args.power_alpha,
                i+1
            )
        else:
            logger.info("Evaluating MetaProd2vec model...")
            results = evaluation(train_mp2v, test,
                                 args.size_embedding, 2*args.window_size, args.min_count, args.workers, args.it,
                                 args.sample, args.neg_sample, args.power_alpha, args.k)
            model_name = 'MetaProd2vec_{}_{}_{}_{}_{}_run_{}'.format(
                name,
                str(args.window_size),
                str(args.it),
                str(args.sample),
                str(args.power_alpha),
                str(i+1)
            )
        t.add_row([model_name, 1000*results['hrk_score'], results['ndcg_score']])
    print t.get_string(sortby='HR@10', reversesort=True)
