import csv
csv.field_size_limit(600000)

def main():
    rows = []
    full_rows = []
    ensembl_to_ncbi = {}
    CSV_IN = "Work\\Outputs\\UTRdb_raw_csv.csv"
    DICT_IN = "Work\\Sources\\Ensembl_to_NCBI_Transcript.csv"
    CSV_OUT = "Work\\Outputs\\UTRdb_raw_csv_w_ncbi.csv"

    # read all records
    with open(CSV_IN, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    # getting "new" headers
    headers = list(rows[0].keys())
    full_headers = ["ncbi_id"] + headers

    # read in dictionary
    with open(DICT_IN, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ensembl = row["ensembl_id"].split('.')[0]
            ensembl_to_ncbi[ensembl] = row["ncbi_id"]
    
    # match up NCBI IDs
    for row in rows:
        if row["ensembl_id"] in ensembl_to_ncbi:
            new_row = row
            new_row["ncbi_id"] = ensembl_to_ncbi[row["ensembl_id"]]
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
