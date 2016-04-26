import urllib.request
import urllib.parse
import json
import logging
import sys
from threading import Thread

class App:
    def __init__(self):

        self.logger = logging.getLogger('tickets')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler('tickets.log')
        self.handler.setFormatter(logging.Formatter('[%(asctime)s]: %(message)s'))
        self.logger.addHandler(self.handler)

        self.logger.info("Start")
        self.logger.debug("Arguments: {0}".format(str(sys.argv)))

        self.urls = [
            ("https://avia.yandex.ru/tickets/update/c54_c213_2016-05-08_None_economy_1_0_0_ru/", [
                "U6 264",
                "S7 56",
                "DP 406",
                "DP 408",
                "DP 404",
            ]),
            ("https://avia.yandex.ru/tickets/update/c213_c54_2016-05-08_None_economy_1_0_0_ru/", [
                "U6 265",
                "S7 53",
                "DP 405",
                "DP 407",
                "DP 403",
            ]),
            ("https://avia.yandex.ru/tickets/update/c54_c213_2016-06-10_None_economy_1_0_0_ru/", [
                "U6 264",
                "S7 56",
                "DP 406",
                "DP 408",
                "DP 404",
            ]),
            ("https://avia.yandex.ru/tickets/update/c213_c54_2016-06-10_None_economy_1_0_0_ru/", [
                "U6 265",
                "S7 53",
                "DP 405",
                "DP 407",
                "DP 403",
            ]),
            ("https://avia.yandex.ru/tickets/update/c213_c50_2016-05-08_None_economy_1_0_0_ru/", [
                "S7 301",
                "DP 433",
            ]),
            ("https://avia.yandex.ru/tickets/update/c50_c213_2016-05-08_None_economy_1_0_0_ru/", [
                "S7 306",
                "DP 434",
            ]),
            ("https://avia.yandex.ru/tickets/update/c213_c50_2016-06-10_None_economy_1_0_0_ru/", [
                "SU 1218",
            ]),
            ("https://avia.yandex.ru/tickets/update/c50_c213_2016-06-10_None_economy_1_0_0_ru/", [
                "SU 1395",
            ]),


        ]

    def request_tickets(self):
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        header = {'User-Agent': user_agent}
        for url, flights_of_interest in self.urls:
            thr = Thread(target=self.get_and_parse, args=[(url, flights_of_interest)])
            thr.start()

    def get_and_parse(self, pair):
        url, flights_of_interest = pair
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        page = response.read()
        page = page.decode('utf-8')
        result = json.loads(page)
        for variant in result['variants']:
            if variant['forward'] in flights_of_interest:
                name = variant['forward']
                price = variant['tariff']['value']
                currency = variant['tariff']['currency']
                internal_name = result['reference']['itineraries'][name][0]
                departure = result['reference']['flights'][internal_name]['departure']['local']
                arrival = result['reference']['flights'][internal_name]['arrival']['local']

                self.logger.info("{0}, {1}, {2}, {3}, {4}".format(name,
                                                                  price,
                                                                  currency,
                                                                  departure,
                                                                  arrival
                                                                  ))




app = App()
app.request_tickets()