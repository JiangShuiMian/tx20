# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import random
import json
from itertools import combinations
from cfgs.config import o_train_data, o_test_data, graphsage_data_path_user_graph

trian_click_log_data = os.path.join(o_train_data, "click_log.csv")
test_click_log_data = os.path.join(o_test_data, "click_log.csv")
trian_ad_data_file = os.path.join(o_train_data, "ad.csv")
test_ad_data_file = os.path.join(o_test_data, "ad.csv")

cols = ['user_id', 'creative_id']

train_pairs = pd.read_csv(trian_click_log_data, encoding='utf-8', dtype=int)[cols]
test_pairs = pd.read_csv(test_click_log_data, encoding='utf-8', dtype=int)[cols]
print("训练数据大小: %d" % (train_pairs.shape[0]))
print("测试数据大小: %d" % (test_pairs.shape[0]))

train_ad_data = pd.read_csv(trian_ad_data_file, encoding='utf-8', dtype=object)
test_ad_data = pd.read_csv(test_ad_data_file, encoding='utf-8', dtype=object)
train_ad_data['creative_id'] = train_ad_data['creative_id'].astype(int)
test_ad_data['creative_id'] = test_ad_data['creative_id'].astype(int)

train_pairs = pd.merge(train_pairs, train_ad_data, how='left', on='creative_id')
test_pairs = pd.merge(test_pairs, test_ad_data, how='left', on='creative_id')

train_pairs = train_pairs[['user_id', 'advertiser_id']]
test_pairs = test_pairs[['user_id', 'advertiser_id']]

print(train_pairs.columns)

creative_id_user_list = {}

print("读取训练数据中边。。。")

train_pairs_userids = list(train_pairs['user_id'])
train_pairs_creativeids = list(train_pairs['advertiser_id'])
test_pairs_userids = list(test_pairs['user_id'])
test_pairs_creativeids = list(test_pairs['advertiser_id'])

# creative_id_user_list = {}
#
# print("读取训练数据中边。。。")
#
# train_pairs_userids = list(train_pairs['user_id'])
# train_pairs_creativeids = list(train_pairs['creative_id'])
# test_pairs_userids = list(test_pairs['user_id'])
# test_pairs_creativeids = list(test_pairs['creative_id'])

del train_pairs
del test_pairs

userids = train_pairs_userids + test_pairs_userids
creativeids = train_pairs_creativeids + test_pairs_creativeids

# i = 0
for index, user_id in enumerate(userids):
    creative_id = creativeids[index]
    uids = creative_id_user_list.setdefault(creative_id, set())
    uids.add(user_id)
    # i += 1
    # if i > 1000000:
    #     break

print("构造广告用户字典完成")
print(len(creative_id_user_list))
del userids
del creativeids

# i = 0
# for key, value in creative_id_user_list.items():
#     print(key)
#     print(value)
#     i += 1
#     if i > 100:
#         break

edge_dic = {}
edges = set()
# for _, uids in creative_id_user_list.items():
#     if len(uids) <= 1:
#         continue
#
#     for us in combinations(uids, 2):
#         edge = "u%s_u%s" % (us[0], us[1])
#         # weight = edge_dic.setdefault(edge, 0)
#         # edge_dic[edge] = weight + 1
#         edges.add(edge)

uid_pair_list = []

for _, us in creative_id_user_list.items():
    if len(uids) <= 1:
        continue

    uids = list(sorted(us))
    del us
    uid_num = len(uids)

    for i in range(0, uid_num-1):
        for j in range(i+1, uid_num):
            edge1 = "u%d_u%d" % (uids[i], uids[j])
            # edge2 = "u%s_u%s" % (uids[j], uids[i])
            # edge = None
            #
            # if edge_dic.get(edge1) is not None:
            #     edge = edge1
            # if edge_dic.get(edge2) is not None:
            #     edge = edge2
            #
            # if edge is None:
            #     edge_dic[edge1] = 1
            # else:
            #     weight = edge_dic.setdefault(edge, 0)
            #     edge_dic[edge] = weight + 1
            # edges.add(edge)
            uid_pair_list.append(edge1)

print('uid_pair_list number: %d ' % (len(uid_pair_list))) # 6159459
import collections
count = collections.Counter(uid_pair_list)
print('count number: %d ' % (len(count))) # 6133343
print(count.most_common(10))
# [('u309204_u3426227', 3), ('u528_u11721', 2), ('u528_u30920', 2), ('u528_u32023', 2), ('u528_u36187', 2), ('u528_u56768', 2), ('u528_u73408', 2), ('u528_u81211', 2), ('u528_u83776', 2), ('u528_u93292', 2)]

for up, w in count.most_common():
    edge_dic[up] = w

print('edge number: %d' % (len(edge_dic))) # 6133343


with open(os.path.join(graphsage_data_path_user_graph, "edges.json"), 'w') as f:
    f.write(json.dumps(edge_dic))