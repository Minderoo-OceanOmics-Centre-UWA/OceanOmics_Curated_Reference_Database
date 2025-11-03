from collections import defaultdict
count_dict = defaultdict(int)
for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2and3.CuratedBOLD.fasta'):
#for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta'):
    if not line.startswith('>'): continue
    thisid = line.split(' ')[0].replace('>', '')
    if (line.startswith('>OG') and '[' in line) or ('NBDL' in line):
        # ocean genomes mitogenome

        ll = line.split('[')
        found = False
        for org in ll:
            if 'organism' in org:
                found = True
                org = org.split(']')[0].replace('organism=', '')
                break
        org = org.strip()
        g = org.split(' ')
        genus = g[0]
        species = ' '.join(g[1:])
        assert found, line
    elif line.startswith('>OG') and '[' not in line:
        spec = line.rstrip().split(' ')
        genus, species = spec[1], spec[2]
    elif line.startswith('>COI_M'):
        spec = line.rstrip().split(' ')
        genus, species = spec[3], spec[4]
    else:
        ll = line.split(' ')
        genus, species = ll[2], ll[3]
    try:
        int(species)
        full_name = genus
    except:
        full_name = f'{genus} {species}'
    if '|' in species:
        full_name = genus
    count_dict[full_name] += 1

for g in count_dict:
    print(g + '\t' + str(count_dict[g]))
