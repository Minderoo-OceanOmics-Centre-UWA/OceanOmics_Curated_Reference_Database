#for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2and3.CuratedBOLD.fasta'):
for line in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta'):
    if not line.startswith('>'): continue
    thisid = line.split(' ')[0].replace('>', '')
    if line.startswith('>OG'):
        # ocean genomes mitogenome

        ll = line.split('[')
        found = False
        for org in ll:
            if 'organism' in org:
                found = True
                org = org.split(']')[0].replace('organism=', '')
                break
        assert found
    elif 
