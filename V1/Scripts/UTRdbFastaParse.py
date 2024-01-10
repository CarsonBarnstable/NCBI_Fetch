import csv
csv.field_size_limit(600000)

def main():
    rows = {}
    full_rows = {}
    START_CHAR = ">"
    FASTA_IN = "..\\Data\\UTRdb_raw_file.fasta"
    CSV_OUT = "..\\Outputs\\UTRdb_raw_csv.csv"

    # setup
    headers = ["ensembl_id", "common_name", "fp_len", "tp_len", "five_prime", "three_prime"]
    data = []
    sequence = ""

    # getting counts with 2 only (one CDS)
    two_only = set()
    ensembl_names = {}
    with open(FASTA_IN, 'r') as f:
        for row in f:
            if row.startswith(START_CHAR):
                data = row[1:].split('|')[1:][:-1]
                if data[1] in ensembl_names:
                    ensembl_names[data[1]] = ensembl_names[data[1]] + 1
                else:
                    ensembl_names[data[1]] = 1
    for e in ensembl_names.keys():
        if ensembl_names[e] == 2:
            two_only.add(e)

    # read all records
    with open(FASTA_IN, 'r') as f:
        for row in f:
            if row.startswith(START_CHAR):
                # saving data
                if data and data[1] in two_only:
                    if data[1] not in rows: rows[data[1]] = {}
                    rows[data[1]]["ensembl_id"] = data[1]
                    rows[data[1]]["common_name"] = data[2]
                    if data[0] == "three_prime_utr": rows[data[1]]["three_prime"] = sequence
                    if data[0] == "five_prime_utr":  rows[data[1]]["five_prime"]  = sequence

                # resetting
                data = row[1:].split('|')[1:][:-1]
                sequence = ""
            else:
                sequence = sequence + row.lower().strip()
        if data[0] == "three_prime_utr": rows[data[1]]["three_prime"] = sequence
        if data[0] == "five_prime_utr":  rows[data[1]]["five_prime"]  = sequence
    
    # isolating full rows (sanity check)
    for row in rows.keys():
        if "three_prime" in rows[row] and "five_prime" in rows[row]:
            full_rows[row] = rows[row]

    # getting accurate lengths
    for row in list(full_rows.keys()):
        full_rows[row]["fp_len"] = len(full_rows[row]["five_prime"])
        full_rows[row]["tp_len"] = len(full_rows[row]["three_prime"])
        
    # generating output file    
    with open(CSV_OUT, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

    # filling file
    with open(CSV_OUT, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(list(full_rows.values()))


if __name__ == "__main__":
    main()
