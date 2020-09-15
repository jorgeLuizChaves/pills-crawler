# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import FormRequest
from pills_crawler.settings import NUMBER_OF_ROWS
from pills_crawler.helper.medicine_builder import MedicineBuilder
from pills_crawler.service.nats_publisher import NatsPublisher


NEXT = 0
pages = list(range(1, 872))


class BularioSpider(Spider):
    name = 'bulario'
    # download_timeout = 720
    allowed_domains = ['www.anvisa.gov.br']
    # start_urls = ['http://www.anvisa.gov.br/datavisa/fila_bula/frmResultado.asp']

    def start_requests(self):
        first_page = str(pages.pop(0))
        yield FormRequest("http://www.anvisa.gov.br/datavisa/fila_bula/frmResultado.asp",
                          formdata={'txtPageSize': NUMBER_OF_ROWS, 'hddPageAbsolute': first_page})

    def parse(self, response):
        medicines = response.xpath('/html/body/div/table[2]/tbody/tr')
        print(f'number of rows {len(medicines)}')
        for medicine_row in medicines:
            try:
                medicine = MedicineBuilder(row=medicine_row).build()
                yield medicine
                NatsPublisher().pub(medicine)
            except Exception as err:
                print(err)

        if pages:
            next_page = pages.pop(NEXT)
            print(f'next page is {next_page}')
            yield FormRequest("http://www.anvisa.gov.br/datavisa/fila_bula/frmResultado.asp",
                              formdata={'txtPageSize': NUMBER_OF_ROWS, 'hddPageAbsolute': str(next_page)})
