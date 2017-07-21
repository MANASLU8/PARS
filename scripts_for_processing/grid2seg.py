# -*- coding: utf-8 -*-

__author__ = "Alexander Shipilo"

import os, codecs
import spon_lib.TextGridReader as TextGridReader
import spon_lib.WaveAssistantFuncs.SegWriter as SegWriter
import scipy.io.wavfile as w
def main():
    debug = 0

    conv_hash = {
        "PSENT" : "seg_R2",
        "EDU": "seg_R1",
        "WF": "seg_B2",
        "SR": "seg_G3",
        "FRS": "seg_Y2"
    }


    if not debug:

        filename = r"D:\GIT\DemoCorpus\tests\0005_129.wav"


        grid2seg(filename, conv_hash)
        print("ok")


def grid2seg(filename, conv_hash):
    try:
        filename = os.path.splitext(filename)[0] + ".TextGrid"
        grid = TextGridReader.readGrid(filename, encoding="UTF-8")
        wav_filename = os.path.splitext(filename)[0] + ".wav"

        wav  = w.read(wav_filename)


        for key, value in conv_hash.items():
            try:
                seg_filename = os.path.splitext(filename)[0] + ".{0}".format(value)

                interval_level = grid["levels"][key]

                seg_data = []

                for elem in interval_level:
                    seg_data.append({
                        "nm": elem["nm"],
                        "frm": int(elem["frm"]*wav[0]),
                        "to": int(elem["to"]*wav[0])
                    })
                seg_data = SegWriter.SegToPer(seg_data)

                SegWriter.write_seg(seg_filename, seg_data, sample_rate = wav[0], byte_per_sample = 2, encoding="windows-1251")
                a = 1
            except Exception as err:
                print("Failed to create seg for {0} {1}".format(key, seg_filename))
        a = 1
    except Exception as err:
        print("grid2seg -> {0}".format(err))
if __name__ == "__main__":
    main()