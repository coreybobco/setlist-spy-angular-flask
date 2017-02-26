from crawler.dj import DJCrawler
from crawler.setlist import SetlistCrawler
from pprint import pprint
# from db import neo4j_db
from db.psql_db import PsqlHandler
from migrations import migrator
# from db import neo4j_db


if __name__ == '__main__':
    m = migrator()
    # m.drop_ptables()
    # m.initialize_db(True)

    p = PsqlHandler()
    # djc = DJCrawler()
    # djc.crawl()
    # p.import_dj_csv()
    # slc = SetlistCrawler()
    # slc.crawl()
    p.import_setlist_csv()

    # p.import_all_csv()

    #Get setlist urls test
    #print(slc.get_setlist_urls("https://www.mixesdb.com/w/Category:Jeff_Mills"))

    # setlist_url = "https://www.mixesdb.com/w/2016-04-16_-_Helena_Hauff_@_20_Years_of_Blueprint_Records,_Mantra_Warehouse,_Manchester"
    # track_texts = slc.scrape_setlist_page_for_tracks(setlist_url)
    # track_nodes = slc.parse_tracks(track_texts)
    # pprint(track_nodes)
