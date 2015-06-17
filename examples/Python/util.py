# coding: utf-8
import logging
import os

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


# codifica um string de retorno para cp1252, encoding conhecido pelo Colibri
def codifica_retorno(texto):
    if isinstance(texto, unicode):
        return texto.encode('cp1252')
    return texto.decode('utf-8').encode('cp1252')