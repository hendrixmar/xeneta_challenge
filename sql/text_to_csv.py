import csv

import argparse

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-i", "--InputFile", help="Path of the input file")
parser.add_argument("-o", "--OutputFile", help="Name of the output csv file")
# Read arguments from command line
args = parser.parse_args()

if not args.InputFile:
    raise "Input file was not"
if not args.OutputFile:
    raise "Output file was not"


def process_text(file_name: str, output_file_path: str):
    with open(file_name) as input_file, \
            open(output_file_path, 'w') as output_file:
        headers = next(input_file).strip().split(',')
        writer = csv.writer(output_file)
        writer.writerow(headers)
        # to process a txt file for exporting a region raw file
        if headers == ["slug", "name", "parent_slug"]:
            for line in input_file:
                slug, *name, parent_slug = line.replace('\\N', 'NULL').split()
                writer.writerow([slug, ' '.join(name), parent_slug])

        # to process a txt file for exporting a port raw file
        elif headers == ["code", "name", "parent_slug"]:
            for line in input_file:
                code, *name, parent_slug = line.replace('\\N', 'NULL').split()
                writer.writerow([code, ' '.join(name), parent_slug])

        # to process a txt file for exporting a price raw file
        elif headers == ["orig_code", "dest_code", "day", "price"]:
            for line in input_file:
                writer.writerow(line.split())



print("Pamparas")
process_text(args.InputFile, args.OutputFile)
