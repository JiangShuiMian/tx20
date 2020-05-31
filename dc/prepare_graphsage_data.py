# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import random
import json
from cfgs.config import o_train_data, o_test_data, graphsage_data_path

trian_click_log_data = os.path.join(o_train_data, "click_log.csv")
test_click_log_data = os.path.join(o_test_data, "click_log.csv")

train_user_data = os.path.join(o_train_data, "user.csv")
edges_dic_file = os.path.join(graphsage_data_path, 'edges.json')

FILE_PREFIX_AGE = 'tx-2020-age'
FILE_PREFIX_GENDER = 'tx-2020-gender'

g_file_age = os.path.join(graphsage_data_path, FILE_PREFIX_AGE + "-G.json")
id_map_file_age = os.path.join(graphsage_data_path, FILE_PREFIX_AGE + "-id_map.json")
class_map_file_age = os.path.join(graphsage_data_path, FILE_PREFIX_AGE + "-class_map.json")

g_file_gender = os.path.join(graphsage_data_path, FILE_PREFIX_GENDER + "-G.json")
id_map_file_gender = os.path.join(graphsage_data_path, FILE_PREFIX_GENDER + "-id_map.json")
class_map_file_gender = os.path.join(graphsage_data_path, FILE_PREFIX_GENDER + "-class_map.json")


def get_nx_G():
    cols = ['user_id', 'creative_id']
    user_cols = ['user_id', 'age', 'gender']

    train_pairs = pd.read_csv(trian_click_log_data, encoding='utf-8', dtype=object)[cols]
    test_pairs = pd.read_csv(test_click_log_data, encoding='utf-8', dtype=object)[cols]
    print("训练数据大小: %d" % (train_pairs.shape[0]))
    print("测试数据大小: %d" % (test_pairs.shape[0]))

    # 读用户属性
    user_df = pd.read_csv(train_user_data, encoding='utf-8', dtype=object)

    # 构造userid和creative_ids的字典
    train_userids = list(train_pairs['user_id'].unique())
    test_user_ids = list(test_pairs['user_id'].unique())

    train_creative_ids = list(train_pairs['creative_id'].unique())
    test_creative_ids = list(test_pairs['creative_id'].unique())

    all_user_ids = set(train_userids + test_user_ids)
    all_creative_ids = set(train_creative_ids + test_creative_ids)

    print("训练数据中user id 个数：%d" % (len(train_userids)))
    print("测试数据中user id 个数：%d" % (len(test_user_ids)))
    print("训练和测试数据中user id 总个数：%d" % (len(all_user_ids)))
    print("训练集和测试集中user id 交集个数 %d" % (len(all_user_ids) - (len(train_userids) + len(test_user_ids))))

    print("训练数据中 creative_id 个数：%d" % (len(train_creative_ids)))
    print("训练数据中 creative_id 个数：%d" % (len(test_creative_ids)))
    print("训练和测试数据中 creative_id 总个数：%d" % (len(all_creative_ids)))
    print("训练集和测试集中 creative_id 交集个数 %d" % (len(all_creative_ids) - (len(train_creative_ids) + len(test_creative_ids))))

    # 构造id字典
    user_id_dic = {'u%s'%(uid): index for index, uid in enumerate(all_user_ids)}
    user_num = len(all_user_ids)
    creative_id_dic = {'c%s'%(cid): (user_num + index) for index, cid in enumerate(all_creative_ids)}

    # 合并用户字典和广告字典
    id_map = {**user_id_dic, **creative_id_dic}
    print("id_map keys number: %d" % (len(id_map.keys())))

    # 构造节点label 字典
    age_class_map = {}
    gender_class_map = {}
    for user_info in user_df.iterrows():
        user_id = user_info[1]['user_id']
        key = "u%s"%(user_id)
        age = user_info[1]['age']
        gender = user_info[1]['gender']
        age_class_map[key] = int(age)
        gender_class_map[key] = int(gender)

    # 构造节点属性，train，val， test 字典
    random.shuffle(train_userids)
    num_val = int(0.2 * len(train_userids))
    val_nodes = train_userids[0:num_val]
    train_nodes = train_userids[num_val:]
    node_atts = {"u%s"%(uid):{'val':False, 'test':False} for uid in train_nodes}
    for nd in val_nodes:
        node_atts.setdefault("u%s"%(nd), {'val': True, 'test': False})

    # 补全所有ids
    for maped_id in id_map.keys():
        age_class_map.setdefault(maped_id, 0)
        gender_class_map.setdefault(maped_id, 0)
        node_atts.setdefault(maped_id, {'val': False, 'test': True})

    # 保存id-map
    with open(id_map_file_age, 'w') as f:
        f.write(json.dumps(id_map))

    with open(id_map_file_gender, 'w') as f:
        f.write(json.dumps(id_map))
    del id_map
    print("保存id_map完成")

    # 保存class-map
    with open(class_map_file_age, 'w') as f:
        f.write(json.dumps(age_class_map))

    with open(class_map_file_gender, 'w') as f:
        f.write(json.dumps(gender_class_map))
    del age_class_map
    del gender_class_map
    del user_df
    print("保存age_class_map完成")
    print("保存gender_class_map完成")
    print("读取边字典")

    with open(edges_dic_file, 'r') as f:
        edge_dic = json.load(f)
    print(len(edge_dic.keys()))
    # all_edges = []
    # print("读取训练数据中边。。。")
    # train_pairs['edge'] = 'u%s_c%s' % (train_pairs, train_pairs[])
    # edge_dic = {}
    # train_pairs_userids = train_pairs['user_id']
    # train_pairs_creativeids = train_pairs['creative_id']
    # for index, user_id in enumerate(train_pairs_userids):
    #     # user_id = pair[1]['user_id']
    #     creative_id = train_pairs_creativeids[index]
    #     pair_key = "u%s_c%s" % (user_id, creative_id)
    #     # all_edges.append(pair_key)
    #     weight = edge_dic.setdefault(pair_key, 0)
    #     edge_dic[pair_key] = weight + 1
    # print(len(edge_dic.keys()))
    # del train_pairs
    #
    # print("读取测试数据中边...")
    # for pair in test_pairs.iterrows():
    #     user_id = pair[1]['user_id']
    #     creative_id = pair[1]['creative_id']
    #     pair_key = "u%s_c%s" % (user_id, creative_id)
    #     # all_edges.append(pair_key)
    #     weight = edge_dic.setdefault(pair_key, 0)
    #     edge_dic[pair_key] = weight + 1
    # print(len(edge_dic.keys()))
    # del test_pairs



    print("构建图。。。")
    G = nx.Graph()
    for key, w in edge_dic.items():
        ns = key.split('_')
        node1 = ns[0]
        node2 = ns[1]
        G.add_node(node1, **node_atts.setdefault(node1, {'val': False, 'test': True}))
        G.add_node(node2, **node_atts.setdefault(node2, {'val': False, 'test': True}))
        G.add_edge(node1, node2, weight=w)

    # 保存图到json
    with open(g_file_age, 'w') as f:
        g_dic = json_graph.node_link_data(G)
        f.write(json.dumps(g_dic))

    with open(g_file_gender, 'w') as f:
        g_dic = json_graph.node_link_data(G)
        f.write(json.dumps(g_dic))


if __name__ == '__main__':
    get_nx_G()