# -*- coding: utf-8 -*-
"""
What i currently need to do to not get a cookie website:
    use a real user agent and not scrapy's default
    Change my ip :(
        The blockage is by some sort of id, one of the parameters is the ip, but not all.
        i can still view the site from my browser
        need to understand better how cookies work
"""
import scrapy
OUT_FOLDER = "/mnt/c/Users/bacon/PycharmProjects/scriprap/out"
COLUMN_IDS = ["propery_type", "where_in_isreal", "address", "rent", "rooms", "enterrance_date", "floor"]
OUT_FILE = "rent.csv"


class YadSpider(scrapy.Spider):
    name = 'yad'
    allowed_domains = ['yad2.co.il']
    start_urls = ['http://www.yad2.co.il/Nadlan/rent.php']

    @staticmethod
    def _validate_column(col):
        return True

    def parse(self, response):
        if len(response.css("div")) == 17:
            print("\nFucking cookie website again\n")
            raise IOError
        products = response.css("table.main_table tr.yellow")
        if not len(products):
            # We probably got to the wrong page, save the html and exit
            pass
        for prod in products:
            columns = prod.css('td[onclick^="show_"]::text')
            col_data = {}
            for col_id, col in zip(COLUMN_IDS, columns):
                col_data[col_id] = col.extract().replace("\n", "").replace("\t", "").strip(" ")
            if YadSpider._validate_column(col_data):
                yield col_data
            else:
                import ipdb; ipdb.set_trace()
            # TODO: Follow the link to the next page
        #next_page =

