# OceanOmics Curated Reference Database

This is the OceanOmics curated reference database.

The main file is `OceanGenomes.CuratedNT.NBDLTranche1and2and3.CuratedBOLD.fasta.gz`.

It contains:

- NBDL fish mitogenomes, the first release (14/11/2025)
- UWA OceanOmics Centre/ Ocean Genomes fish mitogenome assemblies
- BOLD, Australian fish families
- NCBI GenBank 12S, 16S, COI, for Australian fish families. See https://github.com/Minderoo-OceanOmics-Centre-UWA/Minderoo_Foundation-OceanOmics-AmpliconReference for that one.

We curate GenBank and BOLD by clustering sequences - in a nutshell, self-blast, then calculate the LCA for each sequence, then identify sequences leading to very high-level LCAs, then removing those sequences. See doAllQC.py

# Commands to build

# NBDL

We now keep sequences without NCBI taxonomy IDs.

```
# in different folders:
find . -name '*mt.fa' -exec cat {} \; | sed 's/  / /g' > all_tranche1_NBDL.mt.fasta
find . -name '*mt.fa' -exec cat {} \; | sed 's/  / /g' > all_tranche2_NBDL.mt.fasta
find . -name '*mt.fa' -exec cat {} \; | sed 's/  / /g' > all_tranche3_NBDL.mt.fasta

cat  all_tranche1_NBDL.mt.fasta all_tranche2_NBDL.mt.fasta all_tranche3_NBDL.mt.fasta > all_tranche123_NBDL.mt.fasta

# fix the french etc. spellings, blast doesn't like those
iconv -f utf-8 -t ascii//translit all_tranche123_NBDL.mt.fasta > ba
mv ba all_tranche123_NBDL.mt.fasta

# remove mislabels based on NBDL assessment - see RProject NBDL_Data_Cleaning
# script also renames two mislabels
# see keepUs.txt

python removeMislabeledNBDL.py

# get NDBI Taxonomy IDs

cat all_tranche123_NBDL.mt.noMislabels.ids_species.txt | taxonkit name2taxid -i 2 | cut -f 1,3 > all_tranche123_NBDL.mt.noMislabels.ids_species.forBlast.txt

```

Now we have two files: all_tranche123_NBDL.mt.noMislabels.fasta and all_tranche123_NBDL.mt.noMislabels.ids_species.forBlast.txt 


# Filtering BOLD

1. Download Chordata FASTA from https://v4.boldsystems.org/index.php/Public_BINSearch?query=Chordata
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

# Download the Ocean Genomes mitogenomes

aws s3 cp --recursive s3://oceanomics/OceanGenomes/analysed-data/mitogenomes/ .

cat *fa *fasta > AllOcGen_mitogenomes.fasta

# All together

```
cat AllOcGen_mitogenomes.fasta 12S.16S.COI.Mitogenomes.fasta all_tranche123_NBDL.mt.noMislabels.fasta 3-Final/Final_database.fasta > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta
cat OceanGenomes_Mitodatabase.taxids.tsv 12S.16S.COI.Mitogenomes.taxids.txt all_tranche12_NBDL.mt.with_taxids.taxids.noMislabels.txt 3-Final/Final_database_taxids.txt > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids

makeblastdb -dbtype nucl -in OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta -parse_seqids -taxid_map OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids
```

# Make stats for downstream QC

```
cat OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids | taxonkit lineage -i 2 | taxonkit reformat -i 3 > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit
python makeStats.py > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids.taxonkit.stats
```


