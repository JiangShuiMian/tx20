# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

from cfgs.config import base_log_path, o_train_data, o_test_data
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s', filename=os.path.join(base_log_path, "data_ee.log"))
loger = logging.getLogger(__name__)

# o_train_data = os.path.join(o_data_path, "train_preliminary/train_preliminary")
# o_test_data = os.path.join(o_data_path, "test/test")


def print_value_counts(df, col_name):
    loger.info("--" * 10 + col_name + "--" * 10)
    loger.info(df[col_name].value_counts())
    loger.info("%s distinct number : %d" % (col_name, len(df[col_name].unique())))


def print_line(name):
    loger.info("*" * 40)
    loger.info("--" + name + "--")
    loger.info("*" * 40)


def read_data():
    user_data = pd.read_csv(os.path.join(o_train_data, "user.csv"), encoding='utf-8')
    print_line("user_data")
    loger.info("user columns:")
    # ['user_id', 'age', 'gender']
    loger.info(user_data.columns)
    for col in user_data.columns:
        print_value_counts(user_data, col)

    ad_data = pd.read_csv(os.path.join(o_train_data, "ad.csv"), encoding='utf-8')
    test_ad_data = pd.read_csv(os.path.join(o_test_data, "ad.csv"), encoding='utf-8')
    ad_data = pd.concat([ad_data, test_ad_data])
    print_line("ad_data")
    loger.info("ad columns:")
    # ['creative_id', 'ad_id', 'product_id', 'product_category', 'advertiser_id', 'industry']
    # loger.info(ad_data.columns)
    # for col in ad_data.columns:
    #     print_value_counts(ad_data, col)

    train_advertiser_ids = set(ad_data.advertiser_id.unique())
    test_advertiser_ids = set(test_ad_data.advertiser_id.unique())
    loger.info("diff advertiser_ids between train and test set number is: %d" % (len(train_advertiser_ids.difference(test_advertiser_ids))))


    click_data = pd.read_csv(os.path.join(o_train_data, "click_log.csv"), encoding='utf-8')
    print_line("click_data")
    loger.info("click columns:")
    # ['time', 'user_id', 'creative_id', 'click_times']
    loger.info(click_data.columns)
    for col in click_data.columns:
        print_value_counts(click_data, col)

    test_click_data = pd.read_csv(os.path.join(o_test_data, "click_log.csv"), encoding='utf-8')

    train_ad_creative_ids = set(list(click_data['creative_id']))
    loger.info("train_ad_creative_ids num: %d" % (len(train_ad_creative_ids)))
    test_ad_creative_ids =  set(list(test_click_data['creative_id']))
    loger.info("test_ad_creative_ids num: %d" % (len(test_ad_creative_ids)))
    loger.info("训练集和测试集 creative_id 交集 num: %d" % (len(train_ad_creative_ids & test_ad_creative_ids)))

    train_user_ids = set(list(click_data['user_id']))
    loger.info("train_user_ids num: %d" % (len(train_user_ids)))
    test_user_ids =  set(list(test_click_data['user_id']))
    loger.info("test_user_ids num: %d" % (len(test_user_ids)))
    loger.info("训练集和测试机 user_id 交集 num: %d" % (len(test_user_ids & train_user_ids)))


if __name__ == '__main__':
    read_data()
