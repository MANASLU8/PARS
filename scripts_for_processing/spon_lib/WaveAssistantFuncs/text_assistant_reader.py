# -*- coding: utf-8 -*-

__author__ = "Alexander Shipilo"
import codecs, os
def read_txt(f_name):
    try:
        fh = None
        fh = codecs.open(f_name, "rb")

        binary = fh.read( os.path.getsize(f_name) )
        text = ""
        flag = False
        for encod in ["UTF-8", "utf-8-sig", "windows-1251", "UTF-16"]:
            try:
                text = binary.decode(encod)
                flag = True
                break
            except Exception as err:
                continue
        if text.startswith("Sentence="):
            text = text[len("Sentence="):]
        if flag:
            return text
        print("Impossible to read file \"{0}\" with appropriate encoding".format(f_name))
        return ""
    except Exception as err:
        print("read_txt -> {0}".format(err))
def write_txt(f_name, text, encoding="windows-1251"):
    try:
        with codecs.open(f_name, "w", encoding=encoding) as wh:
            wh.write(text)
    except Exception as err:
        print("write_txt -> {0}".format(err))