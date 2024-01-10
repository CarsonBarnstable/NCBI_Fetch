# Script Explanations:
## httpPost.py
#### Utilizes the [NCBI's Entrez Database](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch), to gather a collection of Nucleotide sequence details (given a list of NCBI IDs for Identification)
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
#### Given an Output File from the `httpPost.py` Script, Checks all Sequences to Sequences are Properly Counted (STOP codon always included but not counted), and that Lengths of ORF Sequence and Amino Acid sequence align<br>Has option to take note of, then output a separate CSV file including ONLY Full Rows (entries with no non-available absent data)
- Includes Printouts to ensure data is valid:
  - Number of Lengths Calculated should be same as Number of Sequences Saved
  - ORFs all End with one of {`TAA` / `TAG` / `TGA`} aka STOP Codon, or be blank (typically indicated with `.`)
  - Differences in lengths between ORF and AA (tripled) should only ever be 3 (from missing STOP in AA sequence)
- Optionally, will output file that matches input file, but with only rows that have all data available (no blank cells)

## pairingUTRdbCDS.py
#### Details
- 1
- 2
- 3

## UTRdbNCBINaming.py
#### Details
- 1
- 2
- 3

## UTRdbFastaParse.py
#### Details
- 1
- 2
- 3

## dataSetDifference.py
#### Details
- 1
- 2
- 3

## stopCodons.py
#### Details
- 1
- 2
- 3
