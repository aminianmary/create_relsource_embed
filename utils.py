from collections import defaultdict
import codecs

def get_dictionary(wikt_file):
    wikt_dic = defaultdict(set)
    with codecs.open(wikt_file,'r') as reader:
        for l in reader:
            spl = l.strip().split('\t')
            if len(spl)>1:
                de = spl[0]
                en= spl[1]

                if not de in wikt_dic:
                    wikt_dic[de].add(en)
                else:
                    wikt_dic[de].add(en)
    return wikt_dic

def get_words(target, source):
    words = set()
    with codecs.open(target, 'r') as target_reader, codecs.open(source, 'r') as source_reader:
        for line in target_reader:
            spl = line.strip().split('\t')
            if len(spl) > 1:
                t = spl[1]
                words.add(t)
        for line in source_reader:
            spl = line.strip().split('\t')
            if len(spl) > 1:
                t = spl[1]
                words.add(t)
    return words
