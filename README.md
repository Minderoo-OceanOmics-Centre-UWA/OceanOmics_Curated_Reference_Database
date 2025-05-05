# Internal_AmpliconReference
The merger of all of our current mitogenome databases. This is for internal use ONLY.

# Commands to build

```
find . -name '*mt.fa' -exec cat {} \; > all_tranche1_NBDL.mt.fasta
# replaced double spaces by single spaces in vim

# remove one mislabeled species until we figure out what it is
seqkit grep -v -p NBDL-HK3T1ZWHHNEZW8.v1.mt all_tranche1_NBDL.mt.fasta > all_tranche1_NBDL.mt.noMislabel.fasta

# fix the french etc. spellings, blast doesn't like those
iconv -f utf-8 -t ascii//translit all_tranche1_NBDL.mt.noMislabel.fasta > ba
mv ba all_tranche1_NBDL.mt.noMislabel.fasta

# get the taxids
python getTaxonomyIDs.py

# remove sequences without taxids
grep -P '\t[0-9]' all_tranche1_NBDL.mt.noMislabel.taxids.txt > all_tranche1_NBDL.mt.noMislabel.taxids.with_taxids.txt
seqkit grep  -f <(cut -f 1 all_tranche1_NBDL.mt.noMislabel.taxids.with_taxids.txt) all_tranche1_NBDL.mt.noMislabel.fasta > all_tranche1_NBDL.mt.noMislabel.with_taxids.fasta
grep -P '\t[0-9]' all_tranche1_NBDL.mt.noMislabel.taxids.txt > all_tranche1_NBDL.mt.noMislabel.taxids.with_taxids.taxids.txt

```

And the same for tranche2, just without the removal

```
find . -name '*mt.fa' -exec cat {} \; > all_tranche2_NBDL.mt.fasta
# replaced double spaces by single spaces in vim

# fix the french etc. spellings, blast doesn't like those
iconv -f utf-8 -t ascii//translit all_tranche2_NBDL.mt.fasta > ba
mv ba all_tranche2_NBDL.mt.fasta

# get the taxids
python getTaxonomyIDs.py

# remove sequences without taxids
grep -P '\t[0-9]' all_tranche2_NBDL.mt.taxids.txt > all_tranche2_NBDL.mt.taxids.with_taxids.txt
seqkit grep  -f <(cut -f 1 all_tranche2_NBDL.mt.taxids.with_taxids.txt) all_tranche2_NBDL.mt.fasta > all_tranche2_NBDL.mt.with_taxids.fasta
grep -P '\t[0-9]' all_tranche2_NBDL.mt.taxids.txt > all_tranche2_NBDL.mt.taxids.with_taxids.taxids.txt
```


Remove 5% potential mislabels

```
cat all_tranche1_NBDL.mt.noMislabel.with_taxids.fasta all_tranche2_NBDL.mt.with_taxids.fasta > all_tranche12_NBDL.mt.with_taxids.fasta
cat all_tranche1_NBDL.mt.noMislabel.taxids.with_taxids.taxids.txt all_tranche2_NBDL.mt.taxids.with_taxids.taxids.txt > all_tranche12_NBDL.mt.with_taxids.taxids.txt

python removeMislabeledNBDL.py
```

Now we have two files: all_tranche12_NBDL.mt.with_taxids.noMislabels.fasta and  all_tranche12_NBDL.mt.with_taxids.taxids.noMislabels.txt


# Filtering BOLD

1. Download Chordata FASTA from https://boldsystems.org/index.php/Public_BINSearch?query=Chordata
2. Use taxonkit to pull out families:
    grep '>' BOLD_Chordata.fas | sed  's/|/\t/g' | cut -f 1,2 | taxonkit name2taxid -i 2 | taxonkit lineage -i 3 | taxonkit reformat -i 4 > BOLD_Chordata.taxids.txt
3. Gzip the thing:
    gzip BOLD_Chordata.fas
4. And run the code that removes non-Australian families:
    python filterBOLD.py
5. Re-pull out the taxon IDs:
    grep '>' BOLD_Chordata_Australian_families_only.fasta | sed  's/|/\t/g' | cut -f 1,2 | taxonkit name2taxid -i 2 | taxonkit lineage -i 3 | taxonkit reformat -i 4 > BOLD_Chordata_Australian_families_only.taxids.txt
6. run the QC script:
    python doAllQC.py

# All together

```
cat OceanGenomes_Mitodatabase.fasta 12S.16S.COI.Mitogenomes.fasta all_tranche12_NBDL.mt.with_taxids.noMislabels.fasta 3-Final/Final_database.fasta > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta
cat OceanGenomes_Mitodatabase.taxids.tsv 12S.16S.COI.Mitogenomes.taxids.txt all_tranche12_NBDL.mt.with_taxids.taxids.noMislabels.txt 3-Final/Final_database_taxids.txt > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids

makeblastdb -dbtype nucl -in OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta -parse_seqids -taxid_map OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids
```

# Make stats for downstream QC

```
cat OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids | taxonkit lineage -i 2 | taxonkit reformat -i 3 > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit
python makeStats.py > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit.stats
```


