# Main Script Explanations:
## httpPost.py
#### Utilizes the [NCBI's Entrez Database](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch), to gather a collection of Nucleotide sequence details (given a list of NCBI IDs for Identification<br>Note: Can also combine known/existing data with the entries queried/retrieved in the resulting output file
- Only requires CSV of NCBI IDs (e.g. [NM_005101](https://www.ncbi.nlm.nih.gov/nuccore/NM_005101)), though can combine additional data linked with given NCBI IDs while generating output file.
  - Allows Customization of which interval of IDs to process ( start pos / number to process )
  - Extracts all needed info from the XML Result, saving directly from the NCBI Database
  - Saves at set interval, as a safeguard to power outages, program crashes, or accidental program stopping
- Creates CSV that includes all details included in input CSV, as well as the Nucleotide's:
  - CDS region start/stop position within nucleotide sequence (both endpoints inclusive)
  - ORF Length (number of pairs within CDS region)
  - Amino Acid Sequence Length (number of amino acid bases) in translation of CDS (NOT including STOP codon)
  - Nucleotide Length (number of bases in entire nucleotide sequence)
  - Amino Acid Translation (Amino Acids that form when ORF is translated w/ standard translation table)
  - ORF Sequence (bare sequence of DNA bases that make up the ORF sequence)

## detailParse.py
#### Given an Output File from the [`httpPost.py`](#httppostpy) Script, checks that all sequences are properly counted & structured (STOP codon always included but not counted), and that Lengths of ORF Sequence and Amino Acid sequence align<br>Note: Has option to take note of, then output a separate CSV file including ONLY Full Rows (entries with no non-available absent data)
- Includes Printouts to ensure data is valid:
  - Number of Lengths Calculated should be same as Number of Sequences Saved
  - ORFs all End with one of {`TAA` / `TAG` / `TGA`} aka STOP Codon, or be blank (typically indicated with `.`)
  - Differences in lengths between ORF and AA (tripled) should only ever be 3 (from missing STOP in AA sequence)
- Optionally, will output file that matches input file, but with only rows that have all data available (no blank cells)

## pairingUTRdbCDS.py
#### Combines two data files (one generated, one found as a resource), pairing information from files on the pairing of NCBI IDs<br>Only keeps data entries that have a matching NCBI ID in both files, so resulting output file will only be those that have "complete full information"
- First input file contains details about a Nucleotide's Five Prime and Three Prime (3' and 5') UTRs, or UnTranslated Regions (that surround the CDS Region) - From the Publicly Accessible [UTRdb 2.0](https://pubmed.ncbi.nlm.nih.gov/36399486/) and adjusted by [`UTRdbFastaParse.py`](#utrdbfastaparsepy) and [`UTRdbNCBINaming.py`](#utrdbncbinamingpy)
- Second input file comes from the [`httpPost.py`](#httppostpy) Script (optionally adjusted by [`detailParse.py`](#detailparsepy))
- Output combines the two files, aligned on the NCBI ID columns (only for entries in BOTH files)

# <br>Smaller Helper Scripts Used:

## UTRdbFastaParse.py
#### Parses the raw FASTA file from the UTRdb Download, saving it into a CSV for faster/easier Python Parsing and Expanding
- Extracts the Five Prime and Three Prime data from raw UTRdb FASTA file
- Determines lengths of each UTR to save alongside information (for easier future filtering)
- Saves all FASTA File information (alongside sequence length information) into CSV for future usage

## UTRdbNCBINaming.py
#### Given the Stock UTRdb CSV (from [`UTRdbFastaParse.py`](#utrdbfastaparsepy) -- indexed on Ensembl IDs by defaut), along with a pairwise translation table from Ensembl IDs to NCBI IDs, adds the NCBI ID key to each row where able
- Ensembl ID to NCBI ID translation table from both bioDBnet's [db2bd tool](https://biodbnet-abcc.ncifcrf.gov/db/db2db.php) and the HUGO Gene Nomenclature Committee's [Custom Downloader](https://www.genenames.org/download/custom/)
- Only adds information to UTRdb data, but strips out any rows that do not have Ensembl/NCBI names (not usable along with [`httpPost.py`](#httppostpy) results)

## dataSetDifference.py
#### Used as a Logic/Sanity Checker, and to determine how useful it would be to combine datasets.<br>Counts the prevelance of Genomes between two datasets, records whether a Gene is in Both Datasets, or just one of the two.
- First Dataset queried was the hg19 dataset (Human Genome version 19), from the NCBI's [Genome Assembly GRCh37](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.13/) and [UCSC's Genome Browser on Human GRCh37/hg19](https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&lastVirtModeType=default&lastVirtModeExtraState=&virtModeType=default&virtMode=0&nonVirtPosition=&position=chr7%3A155592223%2D155605565&hgsid=1868361926_ZDCRFUMwLBhlNZ8oPOhbzJXDHwn4)
- Second file includes pairings of UCSC IDs and NCBI IDs, as well as the Genome's Name & RPKM (Reads per Kilo Base per Million Mapped Reads) - to be used later

## stopCodons.py
#### Reads in a File containing Genome Sequence information, and creates new file including STOP codon symbol (typically `-`) in sequence<br>Can also optionally create parallel output file that only contains "Full" data rows
- Note: only adds STOP codon symbols where expected (does not append symbol to cells without any sequence information)
- Increments Amino Acid Translation Length counter as well, so that "counted length" of Sequence still aligns with "recorded length"
