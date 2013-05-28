from hashlib import sha1
from urllib import unquote
from datetime import datetime
import json


def get_bulk_index_lines(page_title, clicks, timestamp_str, categories=None):
    index_lines = []
    document = {}

    # you can provide a list of categories here
    if categories:
        document["categories"] = categories

    document["page_title"] = unquote(page_title).replace("_", " ")
    document["clicks"] = clicks
    date = datetime.strptime(timestamp_str, "pagecounts-%Y%m%d-%H%M%S")
    document["timestamp"] = date.isoformat()

    index_lines.append(json.dumps({"index": {"_type": "clickdata", "_id":
        sha1(page_title + timestamp_str).hexdigest()}}))
    index_lines.append(json.dumps(document))

    return "\n".join(index_lines)


#
#print get_bulk_index_lines("cool%5D", 78, "pagecounts-20120114-230000",
#    categories=["bla", "blub"])

if __name__ == '__main__':
    import sys

    try:
        print get_bulk_index_lines(sys.argv[2], sys.argv[3], sys.argv[1])
    except:
        print >> sys.stderr, "Error processing: %s" % sys.argv

