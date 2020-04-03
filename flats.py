import scrapy


class FlatSpider(scrapy.Spider):
    name = 'flats'
    url = "https://www.homegate.ch/rent/real-estate/matching-list?ep={}&loc={}"


    def start_requests(self):
        for plz in range(1000, 9900):
            if(plz%1000 != 0):
                formatedUrl = self.url.format(1, plz)
                yield scrapy.Request(url=formatedUrl, callback=self.parse)


    def parse(self, response):
        flats = response.css("a[class^='ResultlistItem_itemLink']")
        pageIndex = int(response.url[response.url.find("ep=")+3:response.url.find("&loc=")])
        plz = response.url[-4:]
        newPageIndex = pageIndex + 1

        if(len(flats) > 0):
            for flat in flats:
                yield {
                  'id': flat.attrib['href'].replace('/rent/', ''),
                  'plz': plz,
                  'price': flat.css("span[class^='ListingPriceSimple_price'] span:nth-child(2)::text").extract_first().replace(u'\u2013', "").replace(",", "").replace(".", ""),
                  'area': flat.css("span[class^='LivingSpace_value']::text").extract_first(),
                  'rooms': flat.css("span[class^='RoomNumber_value']::text").extract_first(),
                  'pageIndex': pageIndex
                }
            yield scrapy.Request(url=self.url.format(newPageIndex, plz))

