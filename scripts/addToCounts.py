lineage_dict = {}
genus_to_keep = [x.rstrip().split(' ')[0] for x in open('IUCN_species.txt')]
for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.species_counts.lineages.tsv'):
    ll = line.split()
    genus, rest = ll[0], ll[1:]
    if genus not in genus_to_keep: continue
    lineage_dict[genus] = rest

print('Species\tCount\tFamily\tOrder\tClass')
for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.species_counts.txt'):
    ll = line.split()
    genus = ll[0]
    if genus not in genus_to_keep: continue
    try:
        lineage =  lineage_dict[genus]
    except:
        lineage = ['NA', 'NA', 'NA']
    if len(ll) == 3:
        print('\t'.join([ll[0] + ' ' + ll[1], ll[2]] + lineage))
    else:
        print('\t'.join([ll[0] + ' sp.', ll[1]] + lineage))
