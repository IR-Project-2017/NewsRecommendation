# Run this file after scraping to import into Elastic Search

from elasticsearch import Elasticsearch

# Open Elastic Search connection
es = Elasticsearch()

file_path = "post_file.txt"
# Open file to import from
import_file = open(file_path, "r")

counter = 0

for line in import_file.readlines():

    # Make sure we skip last newline
    if line == "\n":
        continue

    split_line = line.split("\t")

    doc = {
        "title": split_line[0],
        "url": split_line[1],
        'post_date': split_line[3].rstrip("\n")
    }
    res = es.index(index="testindex", doc_type=split_line[4].rstrip("\n"), id=split_line[2], body=doc)
    counter += 1
    if counter % 1000 == 0:

        print("Done indexing " + str(counter) + " documents...")

print("\nIndexed a total of: " + str(counter) + " documents\n")
