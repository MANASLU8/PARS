# -*- coding: utf-8 -*-
__author__ = 'Root'
import os, codecs

import spon_lib.WaveAssistantFuncs.SegReader as SegReader
import spon_lib.WaveAssistantFuncs.SegWriter as SegWriter

def main():
    debug = True

    #FRS = ["discourse:filler", "discourse:pfiller", "discourse:strfiller"]
    #SR = ["discourse:et", "repair:apprepair","repair:revision","repair:repetition","repair:pwrepetition","repair:placeholder","repair:frstart","reparandum:apprepair","reparandum:revision","reparandum:repetition","reparandum:pwrepetition","reparandum:placeholder","reparandum:frstart","insertion"]
    FRS, SR = read_repairs_list()
    if debug:
        f_name = os.path.join(os.path.dirname(__file__), "data_for_test", "0001_189.txt")

        add_speech_repairs(f_name, FRS,SR)
def read_repairs_list():
    try:
        sr = []
        frs = []
        filename = os.path.join(os.path.dirname(__file__), "speech_repairs_list.txt")
        with open(filename, "rb") as fh:
            splt = fh.read(os.path.getsize(filename)).decode("UTF-8").split("SR:")
            frs = [el.strip() for el in splt[0].replace("FRS:", "").strip().split("\n") if el.strip() != ""]
            sr = [el.strip() for el in splt[1].strip().split("\n") if el.strip() != ""]
        return frs, sr
    except Exception as err:
        print("read_repairs_list -> {0}".format(err))



if __name__ == '__main__':
    main()