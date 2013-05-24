import re
import urllib

base_url = "http://dumps.wikimedia.org/other/pagecounts-raw/"

def get_checksums():
    months = crawl_months()
    return crawl_downloads(months)

def crawl_months():
    main_page = fetch(base_url)
    years = find_years(main_page)
    yearly_months = map(get_months, years)
    return reduce(lambda x,y: x+y, yearly_months)

def crawl_downloads(months):
    monthly_checksums = map(lambda month: match_checksums(month), months)
    return reduce(lambda x,y: x+y, monthly_checksums)

def parse_filenames(html):
    return re.findall("href=\"(pagecounts\-\d*\-\d*\.gz)\".*size (\d*)", html)

def find_years(html):
    return re.findall("href=\"(\d\d\d\d)\".\d\d\d\d", html)

def fetch_year(year):
    return fetch("%s%s" % (base_url, year))

def parse_months(html):
    return re.findall("href=\"(\d\d\d\d)\-(\d\d)\"", html)

def get_months(year):
    return parse_months(fetch_year(year))

def fetch_md5s(year, month):
    text = fetch("%s%s/%s-%s/md5sums.txt" % (base_url, year, year, month))
    tokens = map(lambda a: a.split('  '), text.split('\n'))
    valid = filter(lambda a: len(a) == 2, tokens)
    tuples = map(lambda a: tuple(a[::-1]), valid)
    return dict(tuples)

def fetch_month(year, month):
    return fetch("%s%s/%s-%s/" % (base_url, year, year, month))

def fetch(url):
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    return s

def url(year, month, filename):
    return '%s%s/%s-%s/%s' % (base_url, year, year, month, filename)

def make_row(year, month, filename_size, checksums):
    filename, size = filename_size
    if filename in checksums:
        checksum = checksums[filename]
    else:
        checksum = 'none'
    return (checksum, url(year, month, filename), filename, size)


def match_checksums(year_month):
    year, month = year_month
    html = fetch_month(year, month)
    filenames = parse_filenames(html)
    checksums = fetch_md5s(year, month)
    return map(lambda a: make_row(year, month, a, checksums), filenames)


if __name__ == "__main__":
    checksums = get_checksums()
    lines = map(lambda checksum: " ".join(checksum), checksums)
    print '\n'.join(lines)
