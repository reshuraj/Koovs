# -*- coding: utf-8 -*-
import scrapy
from koovs.items import KoovsItem

class KoovsSpider(scrapy.Spider):
    name = "koovs"
    allowed_domains = ["koovs.com"]
    start_urls = ['http://www.koovs.com/women/brands','http://www.koovs.com/men/brands']

    def parse(self, response):
	BRANDS_XPATH = "//div[contains(@class,'brandsBlockList')]//a//@href"
	brands = response.xpath(BRANDS_XPATH).extract()
	for brand in brands:
		yield scrapy.Request(url=brand,callback=self.items_parse)
	
    def items_parse(self,response):
	ITEM_XPATH = "//div[@class='prodDescp']//a[@class='product_url']//@href"
	items = response.xpath(ITEM_XPATH).extract()
	if items:
		for i in items:
			yield scrapy.Request(i,callback=self.parse_particular) 
	
	NEXT_PAGE_XPATH = "//div[@id='search_page_pagination']//a[position()=(last())]//@href"
	NEXT_PAGE_XPATH_TEXT = "//div[@id='search_page_pagination']//a[position()=(last())]//text()"
	next_page = response.xpath(NEXT_PAGE_XPATH).extract()
	next_page_text = response.xpath(NEXT_PAGE_XPATH_TEXT).extract()
	if next_page and next_page_text == '>':
		yield scrapy.Request(next_page[0],callback=self.parse_particular)

    def parse_particular(self,response):
	BRAND_NAME_XPATH = "//span[@class='brandSection']//a//text()"
	PRODUCT_CODE = "//span[@class='prdDescInfoBlk']//text()"
	ITEM_NAME_XPATH = "//span[@itemprop='name']//text()"
	ITEM_PRICE_XPATH = "//span[@itemprop='price']//text()"
	ITEM_IMAGE_XPATH = "//img[@itemprop='image']//@src"

	product_url = response.url.split('?')[0]
	product_code = response.xpath(PRODUCT_CODE).extract_first().split(' ')[2]
	brand_name = response.xpath(BRAND_NAME_XPATH).extract_first()
	item_name = response.xpath(ITEM_NAME_XPATH).extract_first()
        item_price = response.xpath(ITEM_PRICE_XPATH).extract_first().split(',')
	item_price = ''.join(item_price)
        item_img = response.xpath(ITEM_IMAGE_XPATH).extract_first()

        item = KoovsItem(
	    url = product_url,
	    code = product_code,
	    brand = brand_name,
            name = item_name,
	    price = item_price,
            img = item_img
           
        )
        yield item



