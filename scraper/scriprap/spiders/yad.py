# -*- coding: utf-8 -*-
"""
cookie website state:
    + Changing my ip has an effect
    - randomising user agents seems to has no effect as well
    There is a tiny bit of the cookie loading website at the begining, maybe while this happens there is
     a certain transaction happening between the browser and the server, this only happens in the first page
"""
import scrapy
OUT_FOLDER = "/mnt/c/Users/bacon/PycharmProjects/scriprap/out"
COLUMN_IDS = ["propery_type", "where_in_isreal", "address", "rent", "rooms", "enterrance_date", "floor"]
OUT_FILE = "rent.csv"


class YadSpider(scrapy.Spider):
    name = 'yad'
    allowed_domains = ['yad2.co.il']
    start_urls = ['http://www.yad2.co.il/Nadlan/rent.php', "http://www.yad2.co.il/Nadlan/sales.php",
                  "http://www.yad2.co.il/Nadlan/sales.php?AreaID=&City=&HomeTypeID=&Page=8"]

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

