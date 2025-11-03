
to_keep_IDs = set([x.rstrip() for x in open('keepUs.txt').readlines()])
from Bio import SeqIO
duplicates = ["HXDQPC03J6Z8EP", "HXDQPBYPQNN6FH", "HXDQPBYBNNJG3D", "HR5SFNZ5QTHK8G", 
"HR5SFNWJMTTBJ9", "HK4A8AEZKAKW3W", "HK3T1ZXMQNFC8M", "HK3SZKWQGD98XM", 
"HK3SXDWFH37CBV", "HK3SPRSYMG5GYG", "HK3S9B4RJ39QXB", "HKapolap3RX9CQPZNSR3", 
"HK3QY5NSJ9J3FA", "HK3QD0TSHSJS7Q", "HHG28F40QBATSE", 
"HHG28F0WKBG114"]

duplicates_seen = set()

with open('all_tranche123_NBDL.mt.noMislabels.fasta', 'w') as out, open('all_tranche123_NBDL.mt.noMislabels.ids_species.txt', 'w') as out2:
    for s in SeqIO.parse('all_tranche123_NBDL.mt.fasta', 'fasta'):
        long_id = s.id
        short_id = long_id.split('-')[1].split('.')[0]
        if len(short_id) != 14:
            print(short_id, s.id)
        if short_id in duplicates and short_id not in duplicates_seen:
            # we have a duplicate, but it's from tranche 1 or tranche 2- we do not keep this
            duplicates_seen.add(short_id)
            # now we keep only the 'late'r duplicate in the file of all concatenated tranches
            # in other words, if it was in tranche 2 and in tranche 3, we keep only tranche 3
            continue
        if short_id== 'HK3Q0HASJJA7P2':
            s.description= s.description.replace('Dentiraja', 'Dipturus')
        if short_id == 'HK3PGJA0JRACSE':
            s.description = s.description.replace('Heterodontus zebra', 'Heterodontus marshallae')
            s.description = s.description.replace('Heterodontus_zebra', 'Heterodontus_marshallae')
        if short_id == 'HXDQPBYBNNJG3D':
            s.description = s.description.replace('Apogon carinatus', 'Jaydia carinata')
            s.description = s.description.replace('Apogon_carinatus', 'Jaydia_carinata')

        if short_id in to_keep_IDs:
            out.write(s.format('fasta'))
            # and write out the species name for NCBI Taxonomy IDs
            desc = s.description.split('[')
            found_species = False
            for element in desc:
                if 'organism' in element:
                    found_species = True
                    break

            assert found_species, desc
            species = element.replace(']', '').replace('organism=', '')
            out2.write(f'{s.id}\t{species}\n')
            # >NBDL-HK3SXDV9P2JKDM.v1.mt [organism=Hyporthodus griseofasciatus] [authority=Moore, Wakefield, DiBattista & Newman, 2022] [specimen=ANFC H 3969-10] [sequence-length=16547] [missing-bases=0] [mgcode=2] [topology=circular] [md5sum=5f7f64a205ce832f2cec334b0ea4809e] Hyporthodus griseofasciatus specimen ANFC H 3969-10 mitochondrion
