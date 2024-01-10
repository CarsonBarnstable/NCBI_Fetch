import pip._vendor.requests         # for querying NCBI Entrez
import csv                          # for parsing input/output
import xml.etree.ElementTree as ET  # for filtering web result

def main(sp=None, n=None, i=None):
    """
    Controls main flow of program
    Should all be controllable from the 'controller variables' below
    Written by Carson Barnstable in August 2023 for Omics Research

    Args:
        sp (int, optional): Start position. Defaults to None.
        n (int, optional): Number to process. Defaults to None.
        i (int, optional): Save interval. Defaults to None.
    """
    # controller variables
    START_POS = 1 if not sp else sp     # row in input file to start with
    NUM_TODO = 10 if not n else n       # number of rows in input file to go through
    SAVE_INT = 200 if not i else i      # save interval (for larger datasets) - always saves all
    
    PROGRESS_WIDTH = 100                # progress bar width
    PROGRESS_CHAR = "|"
    DATA_BLANK_CHAR = "."

    CSV_IN_FROM = "Work\\Sources\\UCSC_ID_to_NCBI_ID_and_Beyond.csv"
    CSV_IN_HEADS = ["ucsc_id", "ncbi_id", "common_name", "rpkm"]
    NCBI_ID_INDEX = 1       # NCBI ID index in input file (0-indexed)
    CSV_SAVE_TO = "Work\\Outputs\\records_" + str(START_POS) + "_" + str(NUM_TODO+START_POS) + ".csv"

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # needed URL and record keepers
    ids_and_info = get_details_from_input(CSV_IN_FROM)
    full_url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=", "&rettype=xml&retmode=text")
    headers = CSV_IN_HEADS + ["cds_start", "cds_stop", "aa_len", "orf_len", "nuc_len", "aa_translation", "orf_sequence", "nuc_sequence"]
    records = []

    # initiating progress bar printout
    progress_pos = draw_progress_bar(PROGRESS_WIDTH, PROGRESS_CHAR, START_POS, NUM_TODO, -2)

    # creating save file and writing headers
    create_output_file_w_headers(headers, CSV_SAVE_TO)
    
    # going through all intput file rows (by index)
    for i in range(START_POS, START_POS+NUM_TODO):
        try:
            # gather data for processing
            input_row = ids_and_info[i]                     # for easy/quick access
            ncbi_id = input_row[NCBI_ID_INDEX]              # for easy/quick access
            record = {}                                     # making fresh record dict
            details = get_XML_from_URL(ncbi_id, full_url)   # getting XML from web page

            # pre-populating record details
            for head in headers:                # auto-filling blanks
                record[head] = DATA_BLANK_CHAR 
            for j, h in enumerate(CSV_IN_HEADS):# filling in details from input
                record[h] = input_row[j]

            # getting data from webpage
            get_sequence_details(record, details)                           # retrieves all necessary sequence details from XML
            get_sequence_length_details(record, DATA_BLANK_CHAR)   # calculates all length details from sequences
            records.append(record)                                          # adding record to records

        # catching any errors (often no webpage exists)
        except Exception as e:
            print(ncbi_id + ":" + e)
            progress_pos = 0  # resetting progress bar printout

        # updating progress bar
        progress_pos = draw_progress_bar(PROGRESS_WIDTH, PROGRESS_CHAR, START_POS, NUM_TODO, progress_pos)
        
        # saving if needed
        if records and not i%SAVE_INT:
            write_records_to_output_file(records, headers, CSV_SAVE_TO)

    # finishing progress bar after all complete
    progress_pos = draw_progress_bar(PROGRESS_WIDTH, PROGRESS_CHAR, START_POS, NUM_TODO, -1)
    
    # final saving any scraps
    write_records_to_output_file(records, headers, CSV_SAVE_TO)


def get_details_from_input(CSV_IN):
    """
    Pulls all details from the rows of input CSV file

    Args:
        CSV_IN (str): filename of input CSV file

    Returns:
        list: list of rows of input CSV file
    """
    with open(CSV_IN, newline='') as f:
        reader = csv.reader(f)
        return list(reader)


def get_sequence_details(record, details):
    """
    Given an XML webpage, pulls out wanted info and adds to record for keeping

    Args:
        record (dict): record to update
        details (XML string): sequence details in XML webpage
    """

    # pulling relevant data from query
    for feature in details.findall(".//GBFeature"):
        # determining if feature is a CDS Region
        if feature.find("./GBFeature_key").text == "CDS":
            loc = feature.find("./GBFeature_location").text
            record["cds_start"], record["cds_stop"] = loc.split("..")[:2]
        for qual in feature.findall(".//GBQualifier"):
            # getting AA translation of CDS Region
            if qual.find("./GBQualifier_name").text == "translation":
                record["aa_translation"] = qual.find("./GBQualifier_value").text
    
    # hopefully pulling sequence data as well (if it exists)
    seq = details.find(".//GBSeq_sequence").text
    if seq: record["nuc_sequence"] = seq



def get_sequence_length_details(record, DATA_BLANK_CHAR):
    """
    Counts and summarizes length details of sequences

    Args:
        record (dict): record to update
        DATA_BLANK_CHAR (str): character used to indicate data N/A
    """
    # adding length details
    if record["aa_translation"] != DATA_BLANK_CHAR: record["aa_len"] = len(record["aa_translation"])
    if record["cds_start"] != DATA_BLANK_CHAR and record["cds_stop"] != DATA_BLANK_CHAR:
        record["orf_sequence"] = record["nuc_sequence"][int(record["cds_start"])-1:(int(record["cds_stop"]))]
        record["orf_len"] = len(record["orf_sequence"])
    if record["nuc_sequence"] != DATA_BLANK_CHAR: record["nuc_len"] = len(record["nuc_sequence"])


def get_XML_from_URL(ncbi_id, url_sides):
    """
    Retrieves XML webpage of given NCBI genome

    Args:
        ncbi_id (str): NCBI ID of wanted genome
        url_sides (list): two-element list of Entrez link (to go around ID)

    Returns:
        str: XML version of genome's information
    """
    # querying data from URL
    url = url_sides[0] + ncbi_id + url_sides[1]
    x = pip._vendor.requests.post(url)  # retrieving XML
    details = ET.fromstring(x.text)     # parsing XML
    return details


def create_output_file_w_headers(headers, CSV_OUT):
    """
    Creates an output CSV file with given name and headers

    Args:
        headers (list): list of output CSV's headers
        CSV_OUT (str): name of output CSV file
    """
    with open(CSV_OUT, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

def write_records_to_output_file(records, headers, CSV_OUT):
    """
    Writres recorded records to output file and clears details 'cache list'

    Args:
        records (list of dicts): list of filled details with needed information
        headers (list): list of output CSV's headers
        CSV_OUT (str): name of output CSV file
    """
    with open(CSV_OUT, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(records)
    records = []

def draw_progress_bar(PROGRESS_WIDTH, PROGRESS_CHAR, START_POS, NUM_TODO, index, progression=0):
    """
    Draws progress bar corresponding to records processed vs wanted
        An index of -2 indicates a pre-processing print
        An index of -1 indicates a post-processing print
        An index of 0 or greater is a normal progress bar

    Args:
        PROGRESS_WIDTH (int): Width of progress bar
        PROGRESS_CHAR (str): Character used to indicate progress
        START_POS (int): first record row to process
        NUM_TODO (int): number of record rows to process
        index (int): current record row being processed
        progression (int, optional): _description_. Defaults to 0.

    Returns:
        int: number of progress bar markers filled
    """
    if index == -2:     # indicates pre-process print
        print(" "*(PROGRESS_WIDTH-1) + "|< Processing " + str(NUM_TODO) + " Records...")
        print(PROGRESS_CHAR, end="")
        return progression

    if index == -1:
        print(PROGRESS_CHAR*(PROGRESS_WIDTH-progression-1) + "  Progessing Complete!")

    if index >= 0:
        to_add = ((index-START_POS)*PROGRESS_WIDTH)//NUM_TODO - progression
        if to_add > 0:
            print(PROGRESS_CHAR*to_add, end="")
            progression += to_add
        return progression

if __name__=="__main__":
    main()
