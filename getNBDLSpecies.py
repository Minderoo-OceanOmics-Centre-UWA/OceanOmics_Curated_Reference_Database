from glob import glob

for l in glob('all_*mt.fasta'):
    for line in open(l):
        if not line.startswith('>'): continue
        # >NBDL-HK3R0HK1H7H9R1.v1.mt [organism=Cyclichthys spilostylus] [authority=(Leis & Randall, 1982)] [specimen=ANFC H 7271-01] [sequence-length=16515] [missing-bases=0] [mgcode=2] [topology=circular] [md5sum=203189ccba68388b39f705e3d93a6abc] [species=https://biodiversity.org.au/afd/taxa/Cyclichthys_spilostylus] Cyclichthys spilostylus specimen ANFC H 7271-01 mitochondrion
        ll = line.split('[')
        found = False
        for a in ll:
            if 'organism' in a:
                found = True
                break
        if not found: assert False, 'Not found in %s'%line
        a = a.replace(']', '').split('=')[1]
        print('\t'.join([ll[0].replace('>', ''), a]))
