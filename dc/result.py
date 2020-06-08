# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from cfgs.config import graphsage_data_path_user_graph, res_age_pred_file, res_gender_pred_file, res_subimt_file, o_test_data
import json
import pandas as pd
import random

# 两个的id map 相同
FILE_PREFIX_AGE = 'tx-2020-age'
FILE_PREFIX_GENDER = 'tx-2020-gender'

# test_click_log_data = os.path.join(o_test_data, "click_log.csv")
#
# df_test = pd.read_csv(test_click_log_data, encoding='utf-8')
# all_test_uids = set(df_test['user_id'].unique())

res_pred_dic = {}

with open(res_age_pred_file, 'r') as f:
    for line in f.readlines():
        up = line.split(' ')
        # user_index = int(up[0])
        pred = up[1]
        user_id = up[0] # index2user_map.get(user_index)
        res_pred_dic.setdefault(user_id, {"predicted_age": pred})

with open(res_gender_pred_file, 'r') as f:
    for line in f.readlines():
        up = line.split(' ')
        # user_index = int(up[0])
        pred = up[1]
        user_id = up[0] # index2user_map.get(user_index)
        user_val = res_pred_dic.get(user_id)
        user_val['predicted_gender'] = pred

user_ids = []
predicted_ages = []
predicted_genders = []
for key, v in res_pred_dic.items():
    user_ids.append(key)
    predicted_ages.append(v['predicted_age'])
    predicted_genders.append(v['predicted_gender'])

# 补足uid
# for key in all_test_uids:
#     if key not in user_ids:
#         age = random.choice(list(range(1, 11)))
#         genger = random.choice([0, 1])
#         user_ids.append(key)
#         predicted_ages.append(str(age))
#         predicted_genders.append(str(genger))
#         print("add user id: %s age: %d, gender: %d" % (key, age, genger))


res = pd.DataFrame({'user_id': user_ids, 'predicted_age': predicted_ages, 'predicted_gender': predicted_genders})
res.to_csv(res_subimt_file, encoding='utf-8', sep=',', index=False)