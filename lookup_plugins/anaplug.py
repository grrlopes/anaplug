# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: anaplug
    author: Equipe automação
    version_added: "1.5"
    short_description: Lê arquivo CSV source Produban
    description:
        - O anaplug lookup lê o conteudo do arquivo CSV separado por (ponto e virgula, pipe ou outro separador)
        O anaplug transforma o arquivo csv em dicionario e lê o arquivo linha por linha com base no filtro correpondente
        de chave e valor.
    options:
      coluna:
        description:  column to return (0 index).
        default: "1"
      default:
        description: Retorna um valor padrão, quando não for especificado coluna e variável no playbook.
        default: 'coluna e variável'
      separador:
        description: Campo delimitador, que separa os valores por (ponto e virgula, pipe ou outro separador).
        default: ;
      arquivo:
        description: Nome do arquivo no formato CSV.
"""

EXAMPLES = """
Exemplo de playbook plugin
---
- hosts: all
  vars:
    arquivo: 
      "data_bra.csv"
    conteudo: 
      "{{ lookup('anaplug', 'arquivo={{ arquivo }} separador=| coluna=SERIALNUMBER var1=FOX1612GU2Q' ) }}"
  tasks:
    - name: 
        Debugador
      debug: 
        msg="{{ conteudo }}"
    - name: 
        Valores por filtro
      command: 
        echo {{ item.value }}
      with_dict: 
        "{{ conteudo|default({}) }}"
      when: 
        item.value == "Deployed"
"""

RETURN = """
  _raw:
    description:
      - value(s) retorna os valores em formato dict
"""

import csv
from collections import MutableSequence
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_bytes, to_native, to_text

class LookupModule(LookupBase):
    '''
    Methodo que lê os valores do arquivo
    csv e filtra com base no playbook.
    '''
    def listagem(self, arquivo, separador, coluna, var1):
        '''
        LookupModule nomenclatura padrão para a
        estruturaração e criação do ansible plugins.
        '''
        with open(arquivo, 'r') as v_csv:
            f_csv = csv.DictReader(v_csv, delimiter=to_bytes(separador))
            for valor in f_csv:
                if valor[to_bytes(coluna)] == to_bytes(var1):
                    return valor

    def run(self, terms, variables=None, **args):
        ret = []
        for term in terms:
            params = term.split()
            key = params[1]
            parametro = {
                'coluna': "NAME",
                'var1': "",
                'separador': ";",
                'arquivo': "NONE",
            }
            try:
                for param in params[0:]:
                    nome, value = param.split('=')
                    assert nome in parametro
                    parametro[nome] = value
            except (ValueError, AssertionError) as erro:
                raise AnsibleError(erro)
            arquivo = self.find_file_in_search_path(variables, 'arquivo', parametro['arquivo'])
            var = self.listagem(arquivo, parametro['separador'], \
                parametro['coluna'], parametro['var1'])
            if var is not None:
                ret.append(var)
        return ret

"""
class Executa(LookupModule):
    '''
    Classe para testar o plugin, 
    sem passar pelo ansible.
    '''
    def __init__(self):
        LookupModule.__init__(self)
        self.listagem('../data_bra.csv', 'kkkd')

class Principal(object):
    if __name__ == "__main__":
        Executa()
"""