from optparse import OptionParser
from utils import *
import codecs
import numpy as np

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--source", dest="source", help="source training data", metavar="FILE", default=None)
    parser.add_option("--target", dest="target", help="target training data", metavar="FILE", default=None)
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

    print '\nReading source+target words...'
    words = get_words(options.target, options.source)
    print 'Size: '+ str(len(words)) + '...Done!'
    writer = codecs.open(options.output,'w')

    print'\nGetting relsource embeddings...'
    counter =0
    for t in words:
        counter+=1
        if counter%1000==0:
            print str(counter)+'...'

        wikt_embeddings = []
        if t in external_embedding:
            wikt_embeddings.append(external_embedding[t])
        elif t.lower in external_embedding:
            wikt_embeddings.append(external_embedding[t.lower])

        if t in wikt_dic:
            wikt = wikt_dic[t]
            for s in wikt:
                if s in external_embedding:
                    wikt_embeddings.append(external_embedding[s])
                elif s.title() in external_embedding:
                    wikt_embeddings.append(external_embedding[s.title()])

        elif t.lower() in wikt_dic:
            wikt = wikt_dic[t.lower()]
            for s in wikt:
                if s in external_embedding:
                    wikt_embeddings.append(external_embedding[s])
                elif s.title() in external_embedding:
                    wikt_embeddings.append(external_embedding[s.title()])

        if len(wikt_embeddings)>0:
            wikt_embeddings = np.array(wikt_embeddings)
            wikt_avg = np.average(wikt_embeddings, axis=0)
            writer.write(t+' ')
            for e in wikt_avg:
                writer.write(str(e)+' ')
            writer.write('\n')
    print str(len(words)) +'\nDone!'

    writer.flush()
    writer.close()
