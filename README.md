# OceanOmics Curated Reference Database

This is the OceanOmics curated reference database.

The main file is `OceanGenomes.CuratedNT.withNBDL.CuratedBOLD.fasta.gz`.

It contains:

- NBDL fish mitogenomes, the first release (14/11/2025)
- UWA OceanOmics Centre/ Ocean Genomes fish mitogenome assemblies
- BOLD, Australian fish families
- NCBI GenBank 12S, 16S, COI, for Australian fish families. See https://github.com/Minderoo-OceanOmics-Centre-UWA/Minderoo_Foundation-OceanOmics-AmpliconReference for that one.

We curate GenBank and BOLD by clustering sequences - in a nutshell, self-blast, then calculate the LCA for each sequence, then identify sequences leading to very high-level LCAs, then removing those sequences. See doAllQC.py

# Commands to build

# NBDL

We keep sequences without NCBI taxonomy IDs.

```
# download all mitogenomes from https://nbdl.csiro.au/my-downloads

# unzip and concatenate
cat NBDL*fa > all_nbdl.fa

# fix the french etc. spellings, blast doesn't like those
iconv -f utf-8 -t ascii//translit all_nbdl.fa > ba
mv ba all_nbdl.fa

```


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
cat AllOcGen_mitogenomes.fasta 12S.16S.COI.Mitogenomes.fasta all_nbdl.fa 3-Final/Final_database.fasta > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta
cat OceanGenomes_Mitodatabase.taxids.tsv 12S.16S.COI.Mitogenomes.taxids.txt all_tranche12_NBDL.mt.with_taxids.taxids.noMislabels.txt 3-Final/Final_database_taxids.txt > OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids

makeblastdb -dbtype nucl -in OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.fasta -parse_seqids -taxid_map OceanGenomes.CuratedNT.NBDLTranche1and2.CuratedBOLD.taxids
```
