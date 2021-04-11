# Grab the latest stats from the CDC
import os
from parsel import Selector
from urllib3 import PoolManager, util
from urllib.request import urlretrieve
from dateutil import parser
from sys import exit
import aggregate

http = PoolManager()
CDC_URL = 'https://www.cdc.gov/coronavirus/2019-ncov/transmission/variant-cases.html'


if __name__ == '__main__':
    res = http.request('GET', CDC_URL)
    sel = Selector(text=res.data.decode('utf-8'))
    partial_url = util.parse_url(sel.xpath('//a[contains(@href, ".csv")]')[0].attrib['href'])
    last_updated = parser.isoparse(sel.xpath('//meta[@name="cdc:last_published"]')[0].attrib['content']).date()
    filename = f'updates/{last_updated.isoformat()}.csv'
    url = util.Url(scheme='https', host='www.cdc.gov', path=partial_url.path, query=partial_url.query)
    if os.path.exists(filename):
        print('warning: no new updates')
        exit(1)
    else:
        urlretrieve(url.url, filename)
        aggregate.run()
        exit(0)
