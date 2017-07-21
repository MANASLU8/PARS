# -*- coding: utf-8 -*-

__author__ = "Alexander Shipilo"
import os, re, pandas as pd


def main():
    base_dir = r"E:\Dropbox\R Statistics ITMO\tables"
    filenames = ["SpeechProPhone.csv", "ITMO_corpus.csv"]
    outpt_filename = os.path.join(base_dir, "all_repairs.csv")

    outpt = []
    for filename in filenames:
        print(filename)
        filename = os.path.join(base_dir, filename)
        df = pd.read_csv(filename, sep="\t", encoding="UTF-8")


        df_gr = df.groupby(["corpus_name", "filename"])
        for repair_ind in range(1, 6):

            for (name1, name2), group in df_gr:
                one_string = " | ".join( group["ede_text"] )

                new_frm = 0
                while True:
                    try:
                        index_from = one_string.index("!{0}".format(repair_ind), new_frm)
                        index_to =  one_string.index("!{0}".format(repair_ind), index_from+1)
                        outpt.append({
                            "corpus": name1,
                            "filename": "!{0}".format(os.path.basename(name2)),
                            "rep_type": repair_ind,
                            "rep_text": re.sub(r"[.,?]", "", one_string[index_from+2:index_to]),
                        })
                        new_frm = index_to+2
                    except Exception as err:
                        break

    pd.DataFrame(outpt, columns = ["corpus", "filename", "rep_type", "rep_text"]).to_csv(outpt_filename, sep="\t", encoding="UTF-8", index=False)
    a = 1


if __name__ == '__main__':
    main()