# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import random
import json
import numpy as np
from gensim.models import Word2Vec
from cfgs.config import o_train_data, o_test_data, graphsage_data_path_user_graph

FILE_PREFIX_AGE = 'tx-2020-age'
FILE_PREFIX_GENDER = 'tx-2020-gender'

features_file_gender = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_GENDER + "-feats.npy")
features_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-feats.npy")

id_map_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-id_map.json")

with open(id_map_file_age, 'r') as f:
    id_map = json.load(f)


trian_click_log_data = os.path.join(o_train_data, "click_log.csv")
test_click_log_data = os.path.join(o_test_data, "click_log.csv")

df_train = pd.read_csv(trian_click_log_data, dtype=str)
df_test = pd.read_csv(test_click_log_data, dtype=str)

df_cl = pd.concat([df_train, df_test], axis=0)

all_cols = ['creative_id', 'ad_id', 'product_id', 'advertiser_id', 'industry']
emb_size = 64
res = np.zeros((len(id_map), emb_size * len(all_cols)))

for index, col in enumerate(all_cols):
    print("index %d: col: %s w2v begin !")
    sentences = df_cl.groupby(['user_id']).apply(lambda x: x[col].tolist()).tolist()
    model = Word2Vec(sentences=sentences, min_count=1, sg=1, window=10, size=emb_size, workers=22, seed=2020, iter=5)

    user_feature = df_cl.groupby(['user_id']).apply(lambda x: np.mean([model[v] for v in x[col].tolist()], axis=0))
    user_feature = user_feature.reset_index()
    user_feature.columns = ['user_id', 'feat']

    for row in user_feature.iterrows():
        userid = row[1]['user_id']
        feat = row[1]['feat']
        start_pos = index * emb_size
        end_pos = emb_size * (index + 1)
        res[id_map.get('u%s'%(userid))][start_pos: end_pos] = np.array(feat)

    print("index %d: col: %s w2v done !")

np.save(features_file_age, res)
np.save(features_file_gender, res)


