# coding: utf-8
import logging
import os
import json

# obtem caminho do plugin
def obter_caminho_plugin():
    cam = os.path.dirname(__file__)
    while not os.path.isdir(cam):
        novo = os.path.dirname(cam)
        if novo == cam:
            return
        cam = novo
    return cam

# cria um logger para seu plugin
def criar_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w+')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    return l


def retornar(**kwargs):
    return json.dumps(kwargs)