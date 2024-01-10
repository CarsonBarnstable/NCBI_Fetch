import csv
csv.field_size_limit(600000)

def main():
    rows = []
    DATA_BLANK_CHAR = "."
    STOP_CODON_CHAR = "-"
    CSV_IN = "Work\\Outputs\\records_0_24135.csv"
    CSV_OUT = "Work\\Outputs\\records_w_stop.csv"
    CSV_OUT_FULL = "Work\\Outputs\\records_full_w_stop.csv"
    full_rows = []

    # read all records
    with open(CSV_IN, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    headers = rows[0].keys()

    # adding in stop codons for those with aa sequences
    for row in rows:
        if row["aa_translation"] != DATA_BLANK_CHAR:
            row["aa_translation"] = row["aa_translation"] + STOP_CODON_CHAR
            row["aa_len"] = int(row["aa_len"]) + 1
            full_rows.append(row)

    # NORMAL FILE (NOT FULL ROWS)
    with open(CSV_OUT, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

    # fill file
    with open(CSV_OUT, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(rows)

    # FULL FILE (YES FULL ROWS)
    with open(CSV_OUT_FULL, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

    # fill file
    with open(CSV_OUT_FULL, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(full_rows)


if __name__ == "__main__":
    main()
