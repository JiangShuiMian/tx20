# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import random
import json
from cfgs.config import o_train_data, o_test_data, graphsage_data_path_user_graph

trian_click_log_data = os.path.join(o_train_data, "click_log.csv")
test_click_log_data = os.path.join(o_test_data, "click_log.csv")

cols = ['user_id', 'creative_id']

train_pairs = pd.read_csv(trian_click_log_data, encoding='utf-8', dtype=object)[cols]
test_pairs = pd.read_csv(test_click_log_data, encoding='utf-8', dtype=object)[cols]
print("训练数据大小: %d" % (train_pairs.shape[0]))
print("测试数据大小: %d" % (test_pairs.shape[0]))

creative_id_user_list = {}

print("读取训练数据中边。。。")

train_pairs_userids = train_pairs['user_id']
train_pairs_creativeids = train_pairs['creative_id']
for index, user_id in enumerate(train_pairs_userids):
    # user_id = pair[1]['user_id']
    creative_id = train_pairs_creativeids[index]
    # pair_key = "u%s_c%s" % (user_id, creative_id)
    # # all_edges.append(pair_key)
    # weight = edge_dic.setdefault(pair_key, 0)
    # edge_dic[pair_key] = weight + 1
    uids = creative_id_user_list.setdefault(creative_id, set())
    uids.add(user_id)

# print(len(edge_dic.keys()))
# del train_pairs

print("读取测试数据中边...")
for pair in test_pairs.iterrows():
    user_id = pair[1]['user_id']
    creative_id = pair[1]['creative_id']
    # pair_key = "u%s_c%s" % (user_id, creative_id)
    # all_edges.append(pair_key)
    # weight = edge_dic.setdefault(pair_key, 0)
    # edge_dic[pair_key] = weight + 1
    uids = creative_id_user_list.setdefault(creative_id, set())
    uids.add(user_id)
# print(len(edge_dic.keys()))
# del test_pairs

print(creative_id_user_list)

edge_dic = {}
for _, uids in creative_id_user_list.items():
    [edge_dic.setdefault("u%s_u%s" % (uids[i-1], uids[i]), 1) for i in range(1, len(uids))]

with open(os.path.join(graphsage_data_path_user_graph, "edges.json"), 'w') as f:
    f.write(json.dumps(edge_dic))