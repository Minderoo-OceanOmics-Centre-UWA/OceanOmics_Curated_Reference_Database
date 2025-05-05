
to_remove_IDs = set([x.rstrip() for x in open('NBDL_To_remove.txt').readlines()])
from Bio import SeqIO
remove_us = set()
with open('all_tranche12_NBDL.mt.with_taxids.noMislabels.fasta', 'w') as out:
    for s in SeqIO.parse('all_tranche12_NBDL.mt.with_taxids.fasta', 'fasta'):
        long_id = s.id
        short_id = long_id.split('-')[1].split('.')[0]
        if short_id in to_remove_IDs:
            remove_us.add(long_id)
            continue
        out.write(s.format('fasta'))

with open('all_tranche12_NBDL.mt.with_taxids.taxids.noMislabels.txt', 'w') as out:
    for line in open('all_tranche12_NBDL.mt.with_taxids.taxids.txt'):
        ll = line.split()
        long_id = ll[0]
        if long_id in remove_us:
            continue
        out.write(line)


