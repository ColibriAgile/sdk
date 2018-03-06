# coding: utf-8

"""
    É importante que a versão do cmpkg (Pacote do Colibri) e do arquivo
  COP (plugin em python) sejam a mesma. Para tanto, em seu módulo principal do
  Plugin, faça:
  >> from versao import VERSION
  >> PLUGIN_VERSION = VERSION

  VERSAO.INI -  Neste arquivo de seu projeto você deve definir:

  [versaoinfo]
  MajorVersion = 1
  MinorVersion = 0
  Release = 0

  O arquivo versao.py é alimentado da seguinte forma:
  durante o empacotamento para COP, VERSAO.INI será usado para gerar versao.ini
  o número do build virá como parâmetro no fabric, e será gravado automaticamente também.

  >> fab empacotar:build=7

"""

try:
    from __build__ import Build, Develop
except (ImportError, ValueError):
    Build = 0
    Develop = True
try:
    from __version__ import MajorVersion, MinorVersion, Release
except (ImportError, ValueError):
    MajorVersion = 0
    MinorVersion = 0
    Release = 0

VERSION_TUPLE = (MajorVersion, MinorVersion, Release, Build)
VERSION = '.'.join(str(x) for x in VERSION_TUPLE)
