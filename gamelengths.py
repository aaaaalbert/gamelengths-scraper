#!/usr/local/bin/python3


## Metacritic Scraper
# scrapes all game related release information as well as aggregated scores
# for all platforms from the site and writes it to a csv


import urllib.request, urllib.error, urllib.parse
import lxml.html
import csv


# This is where we will output to
output_file = open('gamelengths.csv', 'w')
csv_writer = csv.DictWriter(output_file, fieldnames=["title", "average_length", "times_reported", "platform"], delimiter=';')
csv_writer.writeheader()

base_url = "http://www.gamelengths.com/games/console/"
platforms = ["Playstation+4", "Playstation+3", "Playstation+2", "Playstation", "Playstation+Portable", "Playstation+Vita", "Xbox+One", "Xbox+360", "Microsoft+Xbox", "Wii+U", "Nintendo+Wii", "Gamecube", "Nintendo+64", "Super+Nintendo", "Nintendo", "Nintendo+3DS", "Nintendo+DSi", "Nintendo+DS", "Gameboy+Advance", "Gameboy", "Sega+Dreamcast", "Sega+Saturn", "Sega+GameGear", "Sega+Genesis", "Sega+CD", "iOS", "Mobile", "Android"]

for platform in platforms:
    # while True:
        print("scraping " + platform)
        url = base_url + platform + "/"
        request = urllib.request.Request(url, headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"})
        html = urllib.request.urlopen(request).read()
        root = lxml.html.fromstring(html)

        # Have we reached the end of the search results already?
        # If we have, we'll see the end marker. If not, the xpath
        # selects an empty list.
        # expected_end_marker = root.xpath("//div[@class='module products_module list_product_summaries_module ']/div/div/p[@class='no_data']/text()")
        # try:
        #     if expected_end_marker[0] == "No Results Found":
        #         break
        # except Exception as e:
        #     pass

        # No, not done yet. Continue with products
        products = root.xpath("//div[@class='container']/div[@id='content']/div[2]/table/tbody/tr")

        print(len(products))

        for product in products:
            data = {}

            data['title'] = str(product.xpath("td[2]/a/span/text()")[0])


            times_reported = product.xpath("td[3]/span/text()")
            if len(times_reported) == 0:
                data['times_reported'] = ''
            else:
                data['times_reported'] = str(times_reported[0])

            average_length = product.xpath("td[4]/span/text()")
            if len(average_length) == 0:
                data['average_length'] = ''
            else:
                data['average_length'] = str(average_length[0])


            data['platform'] = platform

            print(data)

            csv_writer.writerow(data)

