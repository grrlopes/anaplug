#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
import csv
import argparse
import sys
try:
    import json
except:
    import simplejson as json

def rparsear():
    parsear = argparse.ArgumentParser(description='Ana Descoberta de servico CMDB')

    parsear.add_argument('--file', action='store', dest='filecsv', required=False, \
                            help='Informe o local do arquivo CVS. Ex: /tmp/file.cvs')
    parsear.add_argument('--delimiter', action='store', dest='delim', default='|', \
                            required=False, help='Informe o separador. Ex: ;')
    parsear.add_argument('--search', action='store', dest='search', required=False, \
                            help='Informe o valor a ser pesquisado')
    parsear.add_argument('--column', action='store', dest='column', required=False, \
                            help='Informe a coluna: NAME|ASSETID|COMPANY|DELIVERYUNIT|VIRTUAL DC| \
                            DISTR NTW|ENVIRONMENT|STATUS|CATEGORY|TYPE|ITEM|PROJECT|HOSTNAME|MANAGED| \
                            IP ADDRESS|ADMVE FQDN|IOS_VERSION|MON_REQ|MON_POLICY|TO BE MON|SUPPLIER| \
                            OWNER|AUTH SYS|BL TARGET|OTHER TARGET|COMPL EXCEPTION|RELATIONSHIP_CS|ASSETID_CS| \
                            NAME_CS|CATEGORY_CS|TYPE_CS|ITEM_CS|STATUS_CS|MANUFACTURER|PRODUCT|VERSION| \
                            CE_SC|SC_NAME|SC_ID|SC_TS|TS_NAME|TS_ID|TSERVICE_BSERVICE_RELATION|BS_NAME|BS_ASSETID| \
                            CONTRACT_ID|SERVICE_TYPE|START DATE|END DATE|SERIALNUMBER')
    return parsear.parse_args()

def listagem():
    '''
    Nomenclatura padrão para a
    estruturaração e criação do ansible plugins.
    '''
    argum = rparsear()
    archive = {"telecom":{}}
    hosts = []
    varr = dict()
    try:
        files = open(argum.filecsv, 'rb')
    except IOError as err:
        print "I/O error({0}): {1}".format(err.errno, err.strerror)
        sys.exit(0)
    with files:
        lista = csv.DictReader(files, delimiter=argum.delim)
        for valor in lista:
            if valor[argum.column] == argum.search:
                hosts = valor["ADMVE FQDN"]
                archive["telecom"] = {"hosts": hosts}
                varr["vars"] = valor
                archive["telecom"].update(varr)
        print to_jason(archive)

def to_jason(_dict):
    return json.dumps(_dict, sort_keys=True, indent=2)

def ans_listagem():
    archive = {"telecom":{}}
    hosts = []
    varr = dict()
    try:
        files = open('./data_bra.csv', 'r')
    except IOError as err:
        print "I/O error({0}): {1}".format(err.errno, err.strerror)
        sys.exit(0)
    with files:
        lista = csv.DictReader(files, delimiter="|")
        for valor in lista:
            if valor['ADMVE FQDN'] != 'IPSI_01A10.bs.br.bsch':
                hosts = valor["ADMVE FQDN"]
                archive["telecom"] = {"hosts": hosts}
                varr["vars"] = valor
                archive["telecom"].update(varr)
        print to_jason(archive)

def main():
    argum = rparsear()
    if argum.column is None and argum.search is None \
    and argum.filecsv is None:
        pass
    else:
        listagem()

if __name__ == '__main__':
    main()
