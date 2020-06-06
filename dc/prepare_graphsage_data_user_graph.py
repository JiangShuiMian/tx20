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
trian_ad_data_file = os.path.join(o_train_data, "ad.csv")
test_ad_data_file = os.path.join(o_test_data, "ad.csv")

train_user_data = os.path.join(o_train_data, "user.csv")
edges_dic_file = os.path.join(graphsage_data_path_user_graph, 'edges.json') # 所有的边及权重
nodes_dic_file = os.path.join(graphsage_data_path_user_graph, 'nodes.json') #所有的节点及属性

FILE_PREFIX_AGE = 'tx-2020-age'
FILE_PREFIX_GENDER = 'tx-2020-gender'

g_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-G.json")
id_map_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-id_map.json")
class_map_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-class_map.json")

g_file_gender = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_GENDER + "-G.json")
id_map_file_gender = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_GENDER + "-id_map.json")
class_map_file_gender = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_GENDER + "-class_map.json")


def get_nx_G():
    """
    只使用 user id 构建图
    :return:
    """
    cols = ['user_id', 'creative_id']

    train_pairs = pd.read_csv(trian_click_log_data, encoding='utf-8', dtype=object)[cols]
    test_pairs = pd.read_csv(test_click_log_data, encoding='utf-8', dtype=object)[cols]
    print("训练数据大小: %d" % (train_pairs.shape[0]))
    print("测试数据大小: %d" % (test_pairs.shape[0]))

    # 训练数据大小: 30082771
    # 测试数据大小: 33585512

    # 读用户属性
    user_df = pd.read_csv(train_user_data, encoding='utf-8', dtype=object)

    # 构造userid和creative_ids的字典
    train_userids = list(train_pairs['user_id'].unique())
    test_user_ids = list(test_pairs['user_id'].unique())

    # train_creative_ids = list(train_pairs['creative_id'].unique())
    # test_creative_ids = list(test_pairs['creative_id'].unique())

    all_user_ids = set(train_userids + test_user_ids)
    # all_creative_ids = set(train_creative_ids + test_creative_ids)

    print("训练数据中user id 个数：%d" % (len(train_userids))) #
    print("测试数据中user id 个数：%d" % (len(test_user_ids)))
    print("训练和测试数据中user id 总个数：%d" % (len(all_user_ids)))
    print("训练集和测试集中user id 交集个数 %d" % (len(all_user_ids) - (len(train_userids) + len(test_user_ids))))

    # print("训练数据中 creative_id 个数：%d" % (len(train_creative_ids)))
    # print("训练数据中 creative_id 个数：%d" % (len(test_creative_ids)))
    # print("训练和测试数据中 creative_id 总个数：%d" % (len(all_creative_ids)))
    # print("训练集和测试集中 creative_id 交集个数 %d" % (len(all_creative_ids) - (len(train_creative_ids) + len(test_creative_ids))))

    # 训练数据中user id 个数：900000
    # 测试数据中user id 个数：1000000
    # 训练和测试数据中user id 总个数：1900000
    # 训练集和测试集中user id 交集个数 0
    # 训练数据中 creative_id 个数：2481135
    # 训练数据中 creative_id 个数：2618159
    # 训练和测试数据中 creative_id 总个数：3412772
    # 训练集和测试集中 creative_id 交集个数 -1686522

    # 构造id字典
    id_map = {'u%s'%(uid): index for index, uid in enumerate(all_user_ids)}
    print("id_map keys number: %d" % (len(id_map.keys())))

    # 构造节点label 字典
    age_class_map = {}
    gender_class_map = {}
    for user_info in user_df.iterrows():
        user_id = user_info[1]['user_id']
        key = "u%s" % (user_id)
        age = user_info[1]['age']
        gender = user_info[1]['gender']
        age_class_map[key] = int(age)
        gender_class_map[key] = int(gender)

    # 补全所有ids
    for maped_id in id_map.keys():
        age_class_map.setdefault(maped_id, 0)
        gender_class_map.setdefault(maped_id, 0)

    # 保存id-map
    with open(id_map_file_age, 'w') as f:
        f.write(json.dumps(id_map))

    with open(id_map_file_gender, 'w') as f:
        f.write(json.dumps(id_map))
    print("保存id_map完成")

    # 保存class-map
    with open(class_map_file_age, 'w') as f:
        f.write(json.dumps(age_class_map))

    with open(class_map_file_gender, 'w') as f:
        f.write(json.dumps(gender_class_map))

    print("保存age_class_map完成")
    print("保存gender_class_map完成")
    print("保存节点属性数据")

    # 构造节点属性，train，val， test 字典
    random.shuffle(train_userids)
    num_val = int(0.2 * len(train_userids))
    val_nodes = train_userids[0:num_val]
    train_nodes = train_userids[num_val:]

    print('all user nodes len: %d' % (len(train_userids))) # 900000
    print('train nodes len: %d' % (len(train_nodes))) # 720000
    print('val nodes len: %d' % (len(val_nodes))) # 180000

    node_atts = {"u%s" % (uid): {'val': False, 'test': False} for uid in train_nodes}

    for nd in val_nodes:
        node_atts.setdefault("u%s"%(nd), {'val': True, 'test': False})

    for nd in test_user_ids:
        node_atts.setdefault("u%s" % (nd), {'val': False, 'test': True})

    # 保存节点属性
    with open(nodes_dic_file, 'w') as f:
        f.write(json.dumps(node_atts))


def build_edges():
    #
    # trian_click_log_data = os.path.join(o_train_data, "click_log.csv")
    # test_click_log_data = os.path.join(o_test_data, "click_log.csv")

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

    # middle_col = 'product_category'
    middle_col = 'advertiser_id'

    train_pairs = train_pairs[['user_id', middle_col]]
    test_pairs = test_pairs[['user_id', middle_col]]

    print(train_pairs.columns)

    creative_id_user_list = {}

    print("读取训练数据中边。。。")

    train_pairs_userids = list(train_pairs['user_id'])
    train_pairs_creativeids = list(train_pairs[middle_col])
    test_pairs_userids = list(test_pairs['user_id'])
    test_pairs_creativeids = list(test_pairs[middle_col])

    del train_pairs
    del test_pairs

    userids = train_pairs_userids + test_pairs_userids
    creativeids = train_pairs_creativeids + test_pairs_creativeids

    for index, user_id in enumerate(userids):
        creative_id = creativeids[index]
        uids = creative_id_user_list.setdefault(creative_id, set())
        uids.add(user_id)

    print("构造广告用户字典完成 key: %s, num : %d" % (middle_col, len(creative_id_user_list)))
    # print(len(creative_id_user_list))
    del userids
    del creativeids

    edge_dic = {}
    uid_pair_list = []
    ls = set()

    for _, us in creative_id_user_list.items():
        if len(uids) <= 1:
            continue

        uids = list(sorted(us))
        # del us
        uid_num = len(uids)

        for i in range(0, uid_num-1):
            for j in range(i+1, uid_num):
                edge1 = "u%d_u%d" % (uids[i], uids[j])
                # uid_pair_list.append(edge1)
                ls.add(edge1)

    print('edge num: %d' % (len(ls)))
    print('uid_pair_list number: %d ' % (len(uid_pair_list))) # 6159459
    import collections
    count = collections.Counter(uid_pair_list)
    print('count number: %d ' % (len(count))) # 6133343
    print(count.most_common(10))
    # [('u309204_u3426227', 3), ('u528_u11721', 2), ('u528_u30920', 2), ('u528_u32023', 2), ('u528_u36187', 2), ('u528_u56768', 2), ('u528_u73408', 2), ('u528_u81211', 2), ('u528_u83776', 2), ('u528_u93292', 2)]

    for up, w in count.most_common():
        edge_dic[up] = w

    print('edge number: %d' % (len(edge_dic))) # 使用 cid时：6133343

    with open(os.path.join(graphsage_data_path_user_graph, "edges.json"), 'w') as f:
        f.write(json.dumps(edge_dic))


def build_graph():
    with open(nodes_dic_file, 'r') as f:
        node_atts = json.load(f)

    with open(edges_dic_file, 'r') as f:
        edge_dic = json.load(f)

    print('edge number: %d' % (len(edge_dic.keys())))

    print("构建图。。。")
    G = nx.Graph()
    print("添加节点。。。")
    for node, att in node_atts.items():
        G.add_node(node, att)

    print("添加边。。。")
    for key, w in edge_dic.items():
        ns = key.split('_')
        node1 = ns[0]
        node2 = ns[1]
        # G.add_node(node1, **node_atts.setdefault(node1, {'val': False, 'test': True}))
        # G.add_node(node2, **node_atts.setdefault(node2, {'val': False, 'test': True}))
        G.add_edge(node1, node2, weight=w)

    # 保存图到json
    with open(g_file_age, 'w') as f:
        g_dic = json_graph.node_link_data(G)
        f.write(json.dumps(g_dic))

    with open(g_file_gender, 'w') as f:
        g_dic = json_graph.node_link_data(G)
        f.write(json.dumps(g_dic))


def g_test():
    """
    分析图
    :return:
    """
    G_data = json.load(open(g_file_age))
    G = json_graph.node_link_graph(G_data)
    all_nodes = G.nodes()
    print("all node number: %d" % (len(all_nodes)))
    isolates_node = list(nx.isolates(G))
    print('isolates_node number: %d' % (len(isolates_node)))


if __name__ == '__main__':
    # get_nx_G()
    build_edges()
    build_graph()
    g_test()