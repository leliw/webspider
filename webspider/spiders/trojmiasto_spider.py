from bs4 import BeautifulSoup, Tag
import re
import scrapy
import logging

class TrojmiastoSpider(scrapy.Spider):
    name = "trojmiasto"
    start_urls = ["https://www.trojmiasto.pl/wiadomosci/"]

    def parse(self, response, **kwargs):
        for item in response.css("li.arch-item"):
            url = item.css("a.color04").attrib['href']
            # yield {
            #     "category": item.css("div.category a::text").get(),
            #     "title": item.css("a.color04::text").get(),
            #     "url": url,
            #     'body' : scrapy.Request(url, callback=self.parse_newsContent)
            # }
            yield scrapy.Request(url, callback=self.parse_newsContent, meta=
            {
                "category": item.css("div.category a::text").get(),
                "title": item.css("a.color04::text").get(),
                "url": url,
            })
        # next_page = response.css("a[title=następna]").attrib['href']
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_newsContent(self, response, **kwargs):
        div = response.css('div.newsContent__text').get()
        soup = BeautifulSoup(div, 'html.parser')

        for el in soup.find_all("div", "photoMarker"):
            el.decompose()
        for el in soup.find_all("div", "oglCrosslinkWrapper"):
            el.decompose()
        for el in soup.find_all("div", "newsPoll"):
            el.decompose()
        for el in soup.find_all("ul", "tableOfContents"):
            el.decompose()

        text = soup.get_text().strip()
        text = re.sub(r"([^.!?,\n])\n\n",r"\1.\n", text)
        text = text.replace("\n", " ")
        text = text.replace("  ", " ")
        text = text.replace("  ", " ")
        yield {
            "category": response.meta["category"].replace("\xa0", " "),
            "title": response.meta["title"].replace("\xa0", " "),
            "url": response.meta["url"],
            "body": text.replace("\xa0", " ")
        }

