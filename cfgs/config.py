# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import socket

machine_taitan = 0
machine_local = 1

MACHINE = machine_local

if socket.gethostname() == "user-IW4200-8G":
    MACHINE = machine_taitan

if socket.gethostname() == "LAPTOP-S9EOTR7P":
    MACHINE = machine_local

print("hostname: %s" % (socket.gethostname()))


def _mkdir(path):
    path = path.strip().rstrip("\\")
    exist_path = os.path.exists(path)
    if not exist_path:
        os.makedirs(path)

    return path



def get_base_path():
    if MACHINE == machine_taitan:
        return "/home/wangqiang/wq/x/tx20/"

    if MACHINE == machine_local:
        return "D:\\PycharmProjects\\tx2020-github\\"


def get_x_path(base_path, mode):
    if mode == 'd':
        return _mkdir(os.path.join(base_path, "datas"))
    if mode == 'm':
        return _mkdir(os.path.join(base_path, "models"))
    if mode == 'i':
        return _mkdir(os.path.join(base_path, "ids"))
    if mode == 'l':
        return _mkdir(os.path.join(base_path, "logs"))


_base_path = get_base_path()
data_path = get_x_path(_base_path, 'd')

o_data_path = os.path.join(data_path, "o")
o_train_data = os.path.join(o_data_path, "train_preliminary/train_preliminary")
o_test_data = os.path.join(o_data_path, "test/test")

base_model_path = get_x_path(_base_path, 'm')
base_log_path = get_x_path(_base_path, 'l')

graphsage_data_path = _mkdir(os.path.join(data_path, "gs_datas"))

graphsage_data_path_user_graph = _mkdir(os.path.join(data_path, "gs_datas_user_graph")) # user 构成的图
