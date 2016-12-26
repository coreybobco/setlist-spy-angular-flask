from crawler.crawler import Crawler

class SearchCrawler(Crawler):

    def get_api_search_url(self, search_input):
        # Get the MixesDB search URL for the category of the DJ that was entered
        # This method should handle capitalization & substring queries. TODO: handle when multiple search results
        search_query = "+".join(search_input.split())
        url = self.base_url + "/db/index.php?title=Special%3ASearch&profile=cats&search=" + search_query + "&fulltext=Search"
        tree = self.get_tree(url)
        anchor_text = tree.xpath(
            "//div[@class='searchresults']/ul[1]//div[@class='mw-search-result-heading']/span[@class='search-result-isCat bold']/a/text()")
        if len(anchor_text):
            return anchor_text[0][9:]
        else:
            raise NameError("No search results")