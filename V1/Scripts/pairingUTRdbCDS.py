import csv

csv.field_size_limit(600000)


def main():
    # record keeping
    utr_rows = []
    cds_rows = []
    full_rows = []
    CSV_UTR_IN = "..\\Data\\UTRdb_raw_csv_w_ncbi.csv"
    CSV_CDS_IN = "..\\Outputs\\records_full_w_stop.csv"
    CSV_OUT = "..\\Outputs\\paired_UTRdb_CDS_full_only.csv"

    # read in all utr records
    with open(CSV_UTR_IN, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            utr_rows.append(row)

    # read in all cds records
    with open(CSV_CDS_IN, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cds_rows.append(row)

    # pairwise matching up NCBI IDs
    full_headers = ["ucsc_id", "ncbi_id", "ensembl_id", "common_name", "rpkm", "cds_start", "cds_stop", "aa_len",
                    "orf_len", "nuc_len", "fp_len", "tp_len", "aa_translation", "orf_sequence", "nuc_sequence",
                    "five_prime", "three_prime"]
    for cds_row in cds_rows:
        for utr_row in utr_rows:
            if cds_row["ncbi_id"] == utr_row["ncbi_id"]:
                # for those that match
                new_row = cds_row
                new_row["ensembl_id"] = utr_row["ensembl_id"]
                new_row["fp_len"] = utr_row["fp_len"]
                new_row["tp_len"] = utr_row["tp_len"]
                new_row["five_prime"] = utr_row["five_prime"]
                new_row["three_prime"] = utr_row["three_prime"]
                full_rows.append(new_row)

    # creating new output file
    with open(CSV_OUT, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=full_headers)
        writer.writeheader()

    # fill file
    with open(CSV_OUT, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=full_headers)
        writer.writerows(full_rows)


if __name__ == "__main__":
    main()
