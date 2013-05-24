Download the wikipedia click data.

Crawl for links and MD5 hashes

    $ mkdir data
    $ python crawl_links.py > data/links.txt

Around 47,000 lines sounds right (since 2007/12)

    $ wc files.txt
    47417  189668 7425114 links.txt

Each line looks like this. The format is "hash", "url", "filename", "size (Mb)"

    $ head -1 links.txt
    398db714a481711d6f4783952a382877 http://dumps.wikimedia.org/other/pagecounts-raw/2007/2007-12/pagecounts-20071209-180000.gz pagecounts-20071209-180000.gz 7

We can get the total size. ~3TB

    $ cat links.txt | awk '{ sum += $4; } END { print sum; }'
    3104558

For a month. ~63GB

    $ grep "pagecounts-201302" links.txt | awk '{ sum += $4; } END { print sum; }'
    63069

For a day. ~2.2GB

    $ grep "pagecounts\-20130201" links.txt | awk '{ sum += $4; } END { print sum; }'
    2298

Download at days worth of data.

    $ mkdir archive
    $ grep "pagecounts-20130201-2" data/links.txt | bash fetch.sh archive
