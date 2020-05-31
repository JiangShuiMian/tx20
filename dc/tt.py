# -*- coding:utf-8 -*-

import os
import networkx as nx
import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import collections
import random
import json
from cfgs.config import o_train_data, o_test_data, graphsage_data_path


FILE_PREFIX = 'tx-2020'

g_file = os.path.join(graphsage_data_path, FILE_PREFIX + "-G.json")
id_map_file = os.path.join(graphsage_data_path, FILE_PREFIX + "-id_map.json")
age_class_map_file = os.path.join(graphsage_data_path, FILE_PREFIX + "-age-class_map.json")
gender_class_map_file = os.path.join(graphsage_data_path, FILE_PREFIX + "-gender-class_map.json")


# with open(id_map_file, 'r') as f:
#     ids = json.load(f)
#     print(len(ids))
#
# with open(age_class_map_file, 'r') as f:
#     ids = json.load(f)
#     print(len(ids))
#
# with open(gender_class_map_file, 'r') as f:
#     ids = json.load(f)
#     print(len(ids))
#
# with open(g_file, 'r') as f:
#     g_dic = json.load(f)
#     print(g_dic.keys())
#
#
# with open("D:\\PycharmProjects\\tx2020\\GraphSAGE\\example_data\\toy-ppi-G.json", 'r') as f:
#     d = json.load(f)
#     print(d.keys())

edges_dic_file = os.path.join(graphsage_data_path, 'edges.json')

with open(edges_dic_file, 'r') as f:
    edge_dic = json.load(f)
print(len(edge_dic.keys()))
