import csv  # for parsing input/output
csv.field_size_limit(600000)


def main():

    rows = []
    DATA_BLANK_CHAR = "."
    RECORDS = "..\\Outputs\\records_1_111.csv"
    CSV_OUT = "..\\Outputs\\records_full_only_1_111.csv"
    DO_CSV_OUT = True

    # read all records
    with open(RECORDS, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    headers = rows[0].keys()
    
    # holds counts
    counts = {'aa': 0, 'orf': 0, 'nuc': 0, 'all': 0}
    sequences = {'aa': 0, 'orf': 0, 'nuc': 0, 'all': 0}
    full_rows = []

    for row in rows:
        # counting counts
        if row['aa_len'] != DATA_BLANK_CHAR:
            counts['aa'] = counts['aa'] + 1
        if row['orf_len'] != DATA_BLANK_CHAR:
            counts['orf'] = counts['orf'] + 1
        if row['nuc_len'] != DATA_BLANK_CHAR:
            counts['nuc'] = counts['nuc'] + 1
        if row['aa_len'] != DATA_BLANK_CHAR and row['orf_len'] != DATA_BLANK_CHAR and row['nuc_len'] != DATA_BLANK_CHAR:
            counts['all'] = counts['all'] + 1

        # counting sequences
        if row['aa_translation'] != DATA_BLANK_CHAR:
            sequences['aa'] = sequences['aa'] + 1
        if row['orf_sequence'] != DATA_BLANK_CHAR:
            sequences['orf'] = sequences['orf'] + 1
        if row['nuc_sequence'] != DATA_BLANK_CHAR:
            sequences['nuc'] = sequences['nuc'] + 1
        if row['aa_translation'] != DATA_BLANK_CHAR and row['orf_sequence'] != DATA_BLANK_CHAR and row['nuc_sequence'] != DATA_BLANK_CHAR:
            sequences['all'] = sequences['all'] + 1

        # truly full rows (don't judge)
        if row['aa_len'] != DATA_BLANK_CHAR and row['orf_len'] != DATA_BLANK_CHAR and row['nuc_len'] != DATA_BLANK_CHAR and row['aa_translation'] != DATA_BLANK_CHAR and row['orf_sequence'] != DATA_BLANK_CHAR and row['nuc_sequence'] != DATA_BLANK_CHAR:
            full_rows.append(row)
    
    # to double check counts
    print()
    print("Num of Length Counts:", counts)
    print("Num of Sequences:    ", sequences)
    print("Note: Nums should match ^^\n")

    if DO_CSV_OUT:
        # make file
        with open(CSV_OUT, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

        # fill file
        with open(CSV_OUT, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerows(full_rows)

    # checking STOP codon status
    last_three = set()
    for row in rows:
        last_three.add(row["orf_sequence"][-3:])
    # ensuring all orf sequences end with STOP codon {TAA | TAG | TGA}
    print("All ORF Sequence Endings:", last_three)
    print("Note: should be STOP { TAA / TAG / TGA }, or", DATA_BLANK_CHAR, "(blank)\n")

    # and AA length calculations
    length_diff = set()
    for row in rows:
        if row["aa_len"] != DATA_BLANK_CHAR:
            length_diff.add(int(row["orf_len"]) - int(row["aa_len"])*3)
    # predicted vs actual length between ORF and AA (likely 3)
    print("Different differences in lengths between ORF and AA (tripled)", length_diff)
    print("Note: should only ever be 3 (from missing STOP Amino Acid)\n")

if __name__=="__main__":
    main()
