from crawler.dj import DJCrawler
from crawler.setlist import SetlistCrawler
from seeder.dj import DJSeeder
from pprint import pprint
from db import neo4j_db
from .models import DJ
from db import psql_db, neo4j_db


if __name__ == '__main__':
    # djc = DJCrawler()
    # djc.crawl()



    neo4j_db.wipe()

    # dj_s = DJSeeder()
    # djs.upsert()
    # dj_s.insert_into_neo4j()

    # conn, cursor = psql_db.connect()
    # driver = neo4j_db.connect()
    # session = driver.session()
    #
    # query = '''MATCH (n)
    #         OPTIONAL MATCH (n)-[r]-()
    #         WITH n,r LIMIT 50000
    #         DELETE n,r
    #         RETURN count(n) as deletedNodesCount'''
    # query = 'SELECT * from DJ'
    # cursor.execute(query)
    # conn.commit()
    #
    # session.run(query)
    #
    #
    #
    # conn.close()
    # slc = SetlistCrawler()
    # # slc.crawl()
    #
    # #Get setlist urls test
    # #print(slc.get_setlist_urls("https://www.mixesdb.com/w/Category:Jeff_Mills"))
    #
    # setlist_url = "https://www.mixesdb.com/w/2016-04-16_-_Helena_Hauff_@_20_Years_of_Blueprint_Records,_Mantra_Warehouse,_Manchester"
    # track_texts = slc.scrape_setlist_page_for_tracks(setlist_url)
    # track_nodes = slc.parse_tracks(track_texts)
    # pprint(track_nodes)
