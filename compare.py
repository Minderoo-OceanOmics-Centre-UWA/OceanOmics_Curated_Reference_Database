import pandas as pd
genera = set()
for g in open('OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.species_counts.txt'):

    g = g.rstrip().split()
    genus = g[0]
    genera.add(genus)

# download all species from fishbase
all_fishbase = pd.read_parquet("https://fishbase.ropensci.org/fishbase/species.parquet") 
# and get their taxonomic ranks, too
fams = pd.read_parquet("https://fishbase.ropensci.org/fishbase/families.parquet")

synonyms = pd.read_parquet('https://fishbase.ropensci.org/fishbase/synonyms.parquet')

merged = pd.merge(all_fishbase, fams, on = 'FamCode')[ ['SpecCode', 'Genus', 'Species_x', 'Family', 'Order', 'Class']]
merged = merged.rename(columns = {"Species_x": 'Species'})
merged['Species'] = merged['Genus'] + ' ' + merged['Species']
merged = merged.reset_index() # just doubly making sure

fishbase_genera_to_lineage = {}
for index, row in merged.iterrows():
    fishbase_genera_to_lineage[row['Genus']] = [row['Family'], row['Order'], row['Class']]



worms = pd.read_csv('worms_species.txt.gz', sep = '\t', header = None, names = ['Species', 'Genus', 'Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'g', 'trash', 'sp'])
worms_genera_to_lineage = {}
for index, row in worms.iterrows():
    worms_genera_to_lineage[row['Genus']] = [row['Family'], row['Order'], row['Class']]

worms_species = set(worms['Species'])
# Aaadont
for g in genera:
    try:
        print(g +'\t' + '\t'.join(fishbase_genera_to_lineage[g]))
        continue
    except:

        pass
    try:
        print(g +'\t' + '\t'.join(worms_genera_to_lineage[g]))
    except:
        pass
