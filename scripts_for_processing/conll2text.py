# -*- coding: utf-8 -*-
__author__ = 'Root'


import codecs, os

def main():
    path2conll = r"d:\GIT\DemoCorpus\PARS\demo\conll_paper_examples\0009\0009_47.conll"
    path2txt = r"d:\GIT\DemoCorpus\democorpusprocessing" + os.path.basename(path2conll)

    words_no_punct = get_words_conll(read_conll(path2conll))



def get_words_conll():
    try:
        a = 1
    except Exception as err:
        print("get_words_conll -> {0}".format(err))
def read_conll(filename):
    try:
        outpt = []


        with codecs.open(filename, "r", encoding="UTF-8") as fh:
            for line in fh:
                splt = line.split("\t")
                splt[-1] = splt[-1].strip()
                outpt.append(
                    splt
                )
    except Exception as err:
        print("read_conll -> {0}".format(err))
    finally:
        return outpt


if __name__ == '__main__':
    main()