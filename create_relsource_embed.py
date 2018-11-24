from optparse import OptionParser
from utils import *
import codecs, sys
import numpy as np

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--wikt", dest="wiktionary", help="wiktionary file", metavar="FILE", default=None)
    parser.add_option("--extrn", dest="external_embedding", help="external embedding", metavar="FILE", default=None)
    parser.add_option("--output", dest="output", help="output file", metavar="FILE", default=None)

    (options, args) = parser.parse_args()
    print '\nReading Wiktionary...'
    wikt_dic = get_dictionary(options.wiktionary)
    print 'Read '+ str(len(wikt_dic)) +'  wiktionary entries!'

    print '\nReading English pre-trained embeddings...'
    external_embedding_fp = codecs.open(options.external_embedding, 'r')
    external_embedding_fp.readline()
    external_embedding = {line.split(' ')[0]: [float(f) for f in line.strip().split(' ')[1:]] for line in
                               external_embedding_fp}
    external_embedding_fp.close()
    edim = len(external_embedding.values()[0])
    print 'Read '+ str(len(external_embedding)) +' English entries!'

    writer = codecs.open(options.output,'w')

    print'\nGetting relsource embeddings...'
    counter =0
    target_words_added = set()
    covered = 0
    for t in wikt_dic.keys():
        counter+=1
        if counter%1000==0:
            sys.stdout.write(str(counter)+'...')
        wikt_embeddings = []
        if t in external_embedding:
            wikt_embeddings.append(external_embedding[t])
            target_words_added.add(t)

        for s in wikt_dic[t]:
            target_words_added.add(s)
            if s in external_embedding:
                wikt_embeddings.append(external_embedding[s])
            if s.title() in external_embedding:
                wikt_embeddings.append(external_embedding[s.title()])
            if s.lower() in external_embedding:
                wikt_embeddings.append(external_embedding[s.lower()])

        if len(wikt_embeddings)>0:
            wikt_embeddings = np.array(wikt_embeddings)
            wikt_avg = np.average(wikt_embeddings, axis=0)
            writer.write(' '.join([t] + [str(e) for e in wikt_avg]))
            writer.write('\n')
            covered += 1

    for t in external_embedding.keys():
        if not t in target_words_added:
            writer.write(' '.join([t] + [str(e) for e in external_embedding[t]]))
            writer.write('\n')
    sys.stdout.write('\n')
    print str((100.0 * float(covered)/len(wikt_dic)))
    writer.flush()
    writer.close()
