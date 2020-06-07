# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from cfgs.config import graphsage_data_path_user_graph, res_age_pred_file, res_gender_pred_file, res_subimt_file
import json
import pandas as pd


# 两个的id map 相同
FILE_PREFIX_AGE = 'tx-2020-age'
FILE_PREFIX_GENDER = 'tx-2020-gender'

id_map_file_age = os.path.join(graphsage_data_path_user_graph, FILE_PREFIX_AGE + "-id_map.json")

with open(id_map_file_age, 'r') as f:
    user2index_map = json.load(f)

index2user_map = {value: key.replace('u', '') for key, value in user2index_map.items()}

res_pred_dic = {}

with open(res_age_pred_file, 'r') as f:
    for line in f.readlines():
        up = line.split(' ')
        user_index = int(up[0])
        pred = int(up[1]) + 1
        user_id = index2user_map.get(user_index)
        res_pred_dic.setdefault(user_id, {"predicted_age": pred})

with open(res_gender_pred_file, 'r') as f:
    for line in f.readlines():
        up = line.split(' ')
        user_index = int(up[0])
        pred = int(up[1]) + 1
        user_id = index2user_map.get(user_index)
        user_val = res_pred_dic.get(user_id)
        user_val['predicted_gender'] = pred

user_ids = []
predicted_ages = []
predicted_genders = []
for key, v in res_pred_dic.items():
    user_ids.append(key)
    predicted_ages.append(v['predicted_age'])
    predicted_genders.append(v['predicted_gender'])


res = pd.DataFrame({'user_id': user_ids, 'predicted_age': predicted_ages, 'predicted_gender': predicted_genders})
res.to_csv(res_subimt_file, encoding='utf-8', sep=',', index=False)