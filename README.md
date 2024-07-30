# Internal_AmpliconReference
The merger of all of our current mitogenome databases. This is for internal use ONLY.

# Commands to build

```
find . -name '*mt.fa' -exec cat {} \; > all_tranche1_NBDL.mt.fasta
# replaced double spaces by single spaces in vim

# fix the french etc. spellings, blast doesn't like those
iconv -f utf-8 -t ascii//translit all_tranche1_NBDL.mt.fasta > ba
mv ba all_tranche1_NBDL.mt.fasta

# get the taxids
grep '>'  all_tranche1_NBDL.mt.fasta | cut -f 1,2,3 -d ' ' | sed 's/mt /mt\t/' | sed 's/\[organism=//' | sed 's/\]//'  | sed 's/>//' | taxonkit name2taxid -i 2  | cut -f 1,3 > all_tranche1_NBDL.mt.taxids.txt

# remove sequences without taxids
grep -P '\t[0-9]' all_tranche1_NBDL.mt.taxids.txt > all_tranche1_NBDL.mt.taxids.with_taxids.txt
seqkit grep  -f all_tranche1_NBDL.mt.taxids.with_taxids.txt all_tranche1_NBDL.mt.fasta > all_tranche1_NBDL.mt.with_taxids.fasta
grep -P '\t[0-9]' all_tranche1_NBDL.mt.taxids.txt > all_tranche1_NBDL.mt.taxids.with_taxids.taxids.txt

# chuck it all together
cat OceanGenomes_Mitodatabase.fasta 12S.16S.Mitogenomes.fasta all_tranche1_NBDL.mt.with_taxids.fasta > OceanGenomes.CuratedNT.NBDLTranche1.fasta
cat OceanGenomes_Mitodatabase.taxids.tsv 12S.16S.Mitogenomes.taxids.txt all_tranche1_NBDL.mt.taxids.with_taxids.taxids.txt > OceanGenomes.CuratedNT.NBDLTranche1.taxids

makeblastdb -dbtype nucl -in OceanGenomes.CuratedNT.NBDLTranche1.fasta -parse_seqids -taxid_map OceanGenomes.CuratedNT.NBDLTranche1.taxids
```
