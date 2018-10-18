# -*- coding: UTF-8 -*-
import spon_lib.WaveAssistantFuncs.SegDict as SegDict
import os,re,codecs

def main():
    filename = r"a.seg_B1"
    write_seg(filename, [])
def write_seg(filename, data, sample_rate = 22050, byte_per_sample=2, n_channel = 1, encoding="UTF-8"):
    '''
    Записывает один сег в файл
    На вход
    filename
    data = {'nm', 'frm'}
    '''
    try:
        wh = None
        colour = SegDict.segColours[filename[-6:]]
        wh = codecs.open(filename, 'w', encoding=encoding)

        wh.write("[PARAMETERS]\n")
        wh.write("SAMPLING_FREQ={0}\n".format(sample_rate))
        wh.write("BYTE_PER_SAMPLE={0}\n".format(byte_per_sample))
        wh.write("CODE=0\n")
        wh.write("N_CHANNEL={0}\n".format(n_channel))
        wh.write("N_LABEL={0}\n".format(len(data)))
        wh.write("[LABELS]\n")

        for i in range(len(data)):
            wh.write("{0},{1},{2}\n".format(data[i]["frm"]*byte_per_sample, colour, data[i]["nm"]))

    except Exception as err:
        print('write_seg -> {0}'.format(err))
    finally:
        if wh is not None:
            wh.close()
def SegToPer(seg):
    '''
    На вход массив с периодами
    на выходе массив
    имя, метка
    '''
    try:
        outpt = []

        for i in range(len(seg)):
            outpt.append({"nm": seg[i]["nm"], "frm": seg[i]["frm"]})
            if i == len(seg)-1:
                if "to" in seg[i]:
                    outpt.append({"nm": "", "frm": seg[i]["to"]})
                continue
            if "to" in seg[i] and seg[i+1]["frm"] != seg[i]["to"]:
                outpt.append({"nm": "", "frm": seg[i]["to"]})
        return outpt
    except Exception as err:
        print("SegWriter SegToPer -> {0}".format(err))
        a = 1
if __name__ == '__main__':
    main()

