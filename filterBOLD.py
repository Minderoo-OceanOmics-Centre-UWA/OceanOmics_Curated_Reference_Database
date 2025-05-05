from Bio import SeqIO
import gzip
families_to_keep = set()

for line in open('Australian_families_and_taxids.txt'):
    ll = line.split()
    family = ll[0]
    families_to_keep.add(family)

to_keep = set()
with open('BOLD_Chordata.removed.tsv', 'w') as out,\
        open('BOLD_Chordata_Australian_families_only.fasta', 'w') as out2:
    for line in open('BOLD_Chordata.taxids.txt'):
        ll = line.rstrip().split('\t')
        thisid = ll[0].replace('>', '')
        lineage = ll[-1].split(';')

        if len(lineage) == 1:
            out.write(f'{thisid} has no taxid - species is {lineage}\n')
            continue
        family = lineage[-3]
        if family in families_to_keep:
            to_keep.add(thisid)
        else:
            out.write(f'{thisid} is not included, family {family} outside of scope\n')
            continue

    # using gzip here because of unicode errors in some records - just ignore
    for s in SeqIO.parse(gzip.open('BOLD_Chordata.fas.gz', 'rt', encoding='utf-8', errors='ignore'), 'fasta'):
        thisid = s.id.split('|')[0]
        if thisid in to_keep:
            s.seq = s.seq.replace('-','')
            out2.write(s.format('fasta'))
        #>ABBID025-09	Murina suilla	59489	cellular organisms;Eukaryota;Opisthokonta;Metazoa;Eumetazoa;Bilateria;Deuterostomia;Chordata;Craniata;Vertebrata;Gnathostomata;Teleostomi;Euteleostomi;Sarcopterygii;Dipnotetrapodomorpha;Tetrapoda;Amniota;Mammalia;Theria;Eutheria;Boreoeutheria;Laurasiatheria;Chiroptera;Yangochiroptera;Vespertilionidae;Murina;Murina suilla	Eukaryota;Chordata;Mammalia;Chiroptera;Vespertilionidae;Murina;Murina suilla
