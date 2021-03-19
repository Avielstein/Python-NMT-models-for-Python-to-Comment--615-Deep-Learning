'''
Converts the data distribution to a single db, with the option to delete
individual files from the data directory in order to save disk space.
'''

import json
import os
import sqlite3
import time

import progressbar

DELETE = False
DATA_DIR = './data/'

# Database operations to start up the sqlite database
conn = sqlite3.connect('all_data.db')
c = conn.cursor()
#c.execute('''CREATE TABLE all_data (filename text, code text, comment text)''')

# Deduplicate any code/comment pairs
dedupe_set = set()

start = time.time()
# walk through the data directory
print("Walking projects...")
p = progressbar.ProgressBar(
    len(os.listdir(DATA_DIR))*2)
    #len(os.listdir(DATA_DIR))*2, display_interval=10)
for (dirpath, dirnames, filenames) in os.walk(DATA_DIR):
    for filename in filenames:

        # whenever you get to one of the project's code/comment data files
        if filename.endswith('.json'):

            # open up the file, load the json, close the file.
            fo = open(os.path.join(dirpath, filename), 'rb')
            d = json.load(fo)
            fo.close()

            # get a list of [code,comment,filename] triplets from the json
            filename_code_comment_triplets = d['contents']
            # add them to the output file
            for triplet in filename_code_comment_triplets:
                code = triplet[1]
                comment = triplet[2]
                # sometimes doxygen fails to extract the code or a comment,
                # don't store these pairs in the database
                if code == '' or comment == '':
                    continue
                # sometimes developers copy code/comments exactly from other
                # code. This results in duplication, which we avoid here
                codecomment_pair = hash(code + comment)
                if codecomment_pair in dedupe_set:
                    continue
                # otherwise store the data
                dedupe_set.add(codecomment_pair)
                c.execute("INSERT INTO all_data VALUES (?,?,?)", triplet)

            conn.commit()

    # progress bar update
    #p.tick_and_maybe_show()

print(" ")
print("Database populated")
# Delete the json file from original project's derivatives folder.
# Choosing to enable this option helps reduce the disk space
# consumed by working with this dataset.
if DELETE == True:
    print("Deleting raw files from data directory...")
    os.system('find ' + DATA_DIR + ' -name "*.json" -type f -delete')

end = time.time()
conn.close()
print("Completed in %d seconds" % (end - start))
