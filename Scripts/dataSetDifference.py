import csv  # for parsing input/output
csv.field_size_limit(600000)


def main():

    rows = []
    hg19_names = set()
    CSV_OUT = "Work\\Outputs\\gene_distribution.csv"

    # read all records
    with open('Work\\Sources\\output_hg19_ncbi.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    # get hg19_names
    for row in rows:
        hg19_names.add(row["attribute_geneID"].split("\"")[1])
    

    rows = []
    cb_names = set()
    # read all different records
    with open('Work\\Sources\\UCSC_ID_to_NCBI_ID_and_Beyond.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    # get hg_names
    for row in rows:
        cb_names.add(row[2])

    # get all "possible" names
    OR = hg19_names | cb_names

    # get proportions of each potential location
    tally = {'hg': 0, 'cb': 0, 'both': 0}
    for item in OR:
        if item in hg19_names: tally["hg"] = tally["hg"] + 1
        if item in cb_names: tally["cb"] = tally["cb"] + 1
        if item in hg19_names and item in cb_names: tally["both"] = tally["both"] + 1
    print(tally)

    # make output file
    with open(CSV_OUT, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "hg_19", "cb", "both"])
        for item in OR:
            writer.writerow([item, item in hg19_names, item in cb_names, item in hg19_names and item in cb_names])

if __name__=="__main__":
    main()
