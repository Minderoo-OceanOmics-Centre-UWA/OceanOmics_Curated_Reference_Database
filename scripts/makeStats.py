from collections import defaultdict
spec_dict = defaultdict(int)
genus_dict = defaultdict(int)
for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit'):
    ll = line.rstrip().split('\t')
    # Eukaryota;Chordata;Actinopteri;Tetraodontiformes;Diodontidae;Diodon;Diodon nicthemerus
    if ';' not in ll[-1]: continue
    k, c, a, order, family, genus, species = ll[-1].split(';')
    genus_dict[genus] += 1
    spec_dict[species] += 1

with open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit_species','w') as out:
    out.write('Species\tSpecies count\n')
    for l in spec_dict:
        out.write(f'{l}\t{spec_dict[l]}\n')


with open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit_genus','w') as out:
    out.write('Genus\tGenus count\n')
    for l in genus_dict:
        out.write(f'{l}\t{genus_dict[l]}\n')

