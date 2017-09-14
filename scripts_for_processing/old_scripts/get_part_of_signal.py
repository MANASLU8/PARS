# -*- coding: utf-8 -*-
__author__ = 'Alexander'

import os, codecs, spon_lib.WaveAssistanFuncs.SegReader as SegReader, spon_lib.WaveAssistanFuncs.SegWriter as SegWriter, random
import scipy.io.wavfile as w
def main():
    debug = True

    dir_to_copy = r"d:\GIT\DemoCorpus\slice"
    if not os.path.isdir(dir_to_copy):
        os.mkdir(dir_to_copy)

    if debug:
        filename = r"D:\GIT\itmo_repository\0000\0000.wav"
        extract_and_copy(dir_to_copy, filename)
        a = 1

def extract_and_copy(dir_to_copy, filename):
    try:
        ede_interval = r"seg_R1"
        words_interval = r"seg_B2"
        repair_level = r"seg_Y2"

        wav = w.read(filename)
        seg = SegReader.readSeg(os.path.splitext(filename)[0]+".{0}".format(words_interval), rAllLevels= True)
        SegReader.SegToPer(seg)
        text = read_txt( os.path.splitext(filename)[0]+".txt" )

        f = seg["periods"][ede_interval][0]["frm"]
        t = seg["periods"][ede_interval][-1]["to"] if seg["periods"][ede_interval][-1]["nm"] != "" else seg["periods"][ede_interval][-2]["to"]

        s_part = wav[1][f:t]

        edes = [{"nm": 0, "frm": elem["frm"]-f, "to": elem["to"]-f} for elem in seg["periods"][ede_interval] if f <= elem["frm"] and elem["frm"] < t]
        words = [{"nm":elem["nm"], "frm": elem["frm"]-f, "to": elem["to"]-f} for elem in seg["periods"][words_interval] if f <= elem["frm"] and elem["frm"] < t]
        repairs = [{"nm":elem["nm"], "frm": elem["frm"]-f, "to": elem["to"]-f} for elem in seg["periods"][repair_level] if f <= elem["frm"] and elem["frm"] < t]
        sentences = align_words_and_sentences(text, words)

        edes = get_indexes_ede(edes, sentences[0]["nm"])
        #words = get_indexes_ede(edes, edes[0]["nm"])


        wav_name = os.path.join(dir_to_copy, os.path.splitext( os.path.basename(filename) )[0] + ".wav")
        ede_seg_name = os.path.join(dir_to_copy, os.path.splitext( os.path.basename(filename) )[0] + ".{0}".format(ede_interval) )
        word_seg_name = os.path.join(dir_to_copy, os.path.splitext( os.path.basename(filename) )[0] + ".{0}".format(words_interval) )
        grid_name =  os.path.join(dir_to_copy, os.path.splitext( os.path.basename(filename) )[0] + ".TextGrid" )

        w.write(wav_name, wav[0], s_part)
        SegWriter.write_seg(ede_seg_name, edes, sample_rate= wav[0])
        SegWriter.write_seg(word_seg_name, words, sample_rate= wav[0])


        if sentences[0]["frm"] != 0:
            sentences.append({"frm": 0, "to": sentences[0]["frm"], "nm": ""})
        if words[0]["frm"] != 0:
            words.append({"frm": 0, "to": words[0]["frm"], "nm": ""})
        if edes[0]["frm"] != 0:
            edes.append({"frm": 0, "to": edes[0]["frm"], "nm": ""})


        write_text_grid_from_hash(grid_name, {
            "PSENT": sentences,
            "EDU": edes,
            "WF": words,
            "SR": repairs,
            "FRS": [{"frm": 0, "to": len(s_part)}],
        },
        wav[0],
        len(s_part),
        ["PSENT", "EDU", "WF", "SR"]
        )
        a = 1
    except Exception as err:
        print("extract_and_copy -> {0}".format(err))
def get_indexes_ede(data, sentence):
    try:
        a = 1
        frm = 3*sentence + random.randint(-5,5)
        for i in range(len(data)):
            data[i]["nm"] = frm + i
    except Exception as err:
        print("get_indexes -> {0}".format(err))
    finally:
        return data
def align_words_and_sentences(text, words):
    try:
        words = [elem for elem in words if elem["nm"].strip() != ""]

        outpt = []
        sent_id = random.randint(5, 20)

        for i in range(len(words)):
            if text[i][1] == 1:
                outpt.append({"frm": words[i]["frm"], "to": words[i]["to"], "nm": sent_id})
                sent_id += 1
            if text[i][2] == 2:
                outpt[-1]["to"] = words[i]["to"]


            a = 1
        a = 1
    except Exception as err:
        print("align_words_and_sentences -> {0}".format(err))
    finally:
        return outpt
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
def read_txt(filename):
    try:
        outpt = []
        with codecs.open(filename, "r", encoding="UTF-8") as fh:
            for line in fh:
                if line.strip() == "":
                    continue
                splt = line.strip().replace("\ufeff", "").split(" ")
                ind_outpt = len(outpt)
                for elem in splt:
                    outpt.append([elem, 0, 0])
                outpt[ind_outpt][1] = 1
                outpt[-1][2] = 1
                a = 1

    except Exception as err:
        print("read_txt -> {0}".format(err))
    finally:
        return outpt
if __name__ == '__main__':
    main()