# -*- coding: utf-8 -*-

__author__ = "Alexander Shipilo"


import os, codecs, spon_lib.WaveAssistantFuncs.SegReader as SegReader, spon_lib.WaveAssistantFuncs.SegWriter as SegWriter, random
import scipy.io.wavfile as w

def main():
    debug = 1

    if debug == 0:
        filename = r"D:\GIT\DemoCorpus\Новая папка\democorpusprocessing\0005_129.wav"


        seg2grid(filename)
        print("ok")
    elif debug == 1:
        dirname = r"D:\GIT\DemoCorpus\Новая папка\democorpusprocessing"

        files = [
            "0005_129.wav",
            "0001_189.wav",
            "0001_203.wav"
        ]

        for filename in files:
            fullname = os.path.join(dirname, filename)
            print(fullname)
            seg2grid(fullname)
    elif debug == 2:
        input_dirname = r"D:\GIT\DemoCorpus\Новая папка\democorpusprocessing"

        files = [elem for elem in os.listdir(input_dirname) if elem.strip().endswith(".TextGrid") and elem.strip().endswith("_res.TextGrid")]

        for filename in files:
            fullname = os.path.join(input_dirname, filename)
            print(fullname)
            seg2grid(fullname)


def seg2grid(filename):
    try:
        out_grid = os.path.splitext(filename)[0] + ".TextGrid"

        input_wav = os.path.splitext(filename)[0] + ".wav"
        input_seg = os.path.splitext(filename)[0] + ".seg_B2"

        seg = SegReader.readSeg(input_seg, rAllLevels=True)
        wav = w.read(input_wav)

        SegReader.SegToPer(seg)

        write_text_grid_from_hash(out_grid, {
            "PSENT": [{"frm": 0,  "to": len(wav[1]), "nm": ""}],
            "EDU": seg["periods"].get("seg_R1", [{"frm": 0,  "to": len(wav[1]), "nm": ""}]),
            "WF": seg["periods"]["seg_B2"],
            "SR": seg["periods"].get("seg_G3", [{"frm": 0,  "to": len(wav[1]), "nm": ""}]),
            "FRS": seg["periods"].get("seg_Y2", [{"frm": 0,  "to": len(wav[1]), "nm": ""}]),
        },
        wav[0],
        len(wav[1]),
        ["PSENT", "EDU", "WF", "SR", "FRS"]
        )
    except Exception as err:
        print("seg2grid -> {0}".format(err))

def write_text_grid_from_hash(grid_name, seg, sample_rate, len_signal, levels):
    try:
        w = None
        w = open(grid_name, "w", encoding = "utf8")
        if w is None:
            return
        #chapka
        w.write("File type = \"ooTextFile\"\nObject class = \"TextGrid\"\n\nxmin = 0.0\n")


        xmax = len_signal/sample_rate
        w.write("xmax = {0}\ntiers? <exists>\nsize = {1}\nitem []:\n".format(float(xmax), len(seg)))

        for key in seg.keys():
            if seg[key][0]["frm"] != 0:
                seg[key].insert(0, {"nm": "", "frm": 0, "to": seg[key][0]["frm"]})
            if seg[key][-1]["to"] != len_signal:
                seg[key].append({"frm": seg[key][-1]["to"], "nm": "", "to": len_signal})

        size_total = 0
        ind_level = 1
        for level_name in levels:
            try:
                cur_intervals = seg[level_name]
                w.write("\titem [{0}]\n".format(ind_level))
                w.write("\t\tclass = \"IntervalTier\"\n")
                w.write("\t\tname = \"{0}\"\n".format(level_name))
                w.write("\t\txmin = {0}\n".format(float(cur_intervals[0]["frm"]/sample_rate)))
                w.write("\t\txmax = {0}\n".format(float(xmax)))
                if len(cur_intervals):
                    w.write("\t\tintervals: size = {0}\n".format(len(cur_intervals)))
                    j_ind = 1
                    for item in cur_intervals:
                        w.write("\t\tintervals [{0}]:\n".format(j_ind))
                        w.write("\t\t\txmin = {0}\n".format(float(item["frm"]/sample_rate)))
                        w.write("\t\t\txmax = {0}\n".format(float(item["to"]/sample_rate)))
                        w.write("\t\t\ttext = \"{0}\"\n".format(item["nm"]))
                        j_ind += 1
                else:
                    w.write("\t\tintervals: size = 1\n")
                    w.write("\t\tintervals [1]:\n")
                    w.write("\t\t\txmin = 0\n")
                    w.write("\t\t\txmax = {0}\n".format(float(item["to"]/sample_rate)))
                    w.write("\t\t\ttext = \"\"\n")
                a = 1
            except Exception as err:
                print(err)

    except Exception as err:
        print(err)
    finally:
        if w is not None:
            w.close()
if __name__ == "__main__":
    main()