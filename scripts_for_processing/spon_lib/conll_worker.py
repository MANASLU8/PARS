# -*- coding: utf-8 -*-
__author__ = 'Alexander Shipilo'

import codecs, os
def read_conll(conll_name):
    try:
        outpt = []
        with codecs.open(conll_name, "r", encoding="UTF-8") as fh:
            ind = 1
            for line in fh:
                if line.strip() == "" or line.startswith("#"):
                    ind += 1
                    continue

                splt = line.split()
                splt[-1] = splt[-1].strip()

                outpt.append([splt[1], splt[7]])
                ind += 1
                a = 1
    except Exception as err:
        print("read_conll -> {0}".format(err))
    finally:
        return outpt