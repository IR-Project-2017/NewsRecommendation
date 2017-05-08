# Run this file after scraping to import into Elastic Search

from elasticsearch import Elasticsearch
"""
post_file.txt Format:
Greece reaches preliminary bailout deal with creditors	http://www.france24.com/en/20170502-greece-preliminary-bailout-deal-creditors	68w6qf  2017-04-20	10-19:69,20-29:17,30-39:56,40-49:57,50-59:87,60-69:58,70-79:12,80+:12	worldnews
"""
# Open Elastic Search connection
es = Elasticsearch()

file_path = "post_file.txt"
# Open file to import from
import_file = open(file_path, "r")

counter = 0

for line in import_file.readlines():
    print(line)
    # Make sure we skip last newline
    if line == "\n":
        continue

    split_line = line.split("\t")

    doc = {
        "title": split_line[0].rstrip("\n"),
        "url": split_line[1].rstrip("\n"),
        "post_date": split_line[3].rstrip("\n"),
        "age_groups": {group_object.split(":")[0]: int(group_object.split(":")[1]) for group_object in (group_object_list for group_object_list in split_line[4].split(","))},
        "like": 0,
        "dislike": 0
    }
    # TODO Might wanna change doc_type to all have the same type, and add subreddit to _source
    res = es.index(index="testindex", doc_type=split_line[5].rstrip("\n"), id=split_line[2], body=doc)
    counter += 1
    if counter % 1000 == 0:

        print("Done indexing " + str(counter) + " documents...")

print("\nIndexed a total of: " + str(counter) + " documents\n")
