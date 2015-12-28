#!/usr/local/bin/python3


## Metacritic Scraper
# scrapes all game related release information as well as aggregated scores
# for all platforms from the site and writes it to a csv


import urllib.request, urllib.error, urllib.parse
import lxml.html
import csv


# This is where we will output to
output_file = open('howlongtobeat.csv', 'w')
csv_writer = csv.DictWriter(output_file, fieldnames=["title", "main_story_length", "mainextra_length", "completionist_length", "combined_length", "platform"], delimiter=';')
csv_writer.writeheader()

base_url = "http://howlongtobeat.com/search_main.php?page="
platforms = ['3DO', 'Amiga', 'Amstrad CPC', 'Android', 'Apple II', 'Arcade', 'Atari 2600', 'Atari 5200', 'Atari 7800', 'Atari Jaguar', 'Atari Jaguar CD', 'Atari Lynx', 'Atari ST', 'Browser', 'Commodore 64', 'Dreamcast', 'Game & Watch', 'Game Boy', 'Game Boy Advance', 'Game Boy Color', 'iOS', 'Linux', 'Mac', 'MSX', 'N-Gage', 'Neo Geo', 'Neo Geo CD', 'Neo Geo Pocket', 'Neo Geo Pocket Color', 'NES', 'Nintendo 2DS', 'Nintendo 3DS', 'Nintendo 64', 'Nintendo DS', 'Nintendo GameCube', 'OnLive', 'Ouya', 'PC', 'Philips CD-i', 'PlayStation', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation Now', 'PlayStation Vita', 'PSP', 'Sega 32X', 'Sega CD', 'Sega Game Gear', 'Sega Master System', 'Sega Mega Drive/Genesis', 'Sega Saturn', 'Sharp X68000', 'Super Nintendo', 'Tiger Handheld', 'Turbografx-16', 'Turbografx-CD', 'Virtual Boy', 'Wii', 'Wii U', 'Windows Phone', 'WonderSwan', 'Xbox', 'Xbox 360', 'Xbox One', 'ZX Spectrum']
# platforms = ["3DO"]


for platform in platforms:
    page = 1
    while True:
        print("scraping " + platform + " page " + str(page))

        url = base_url + str(page)
        request = urllib.request.Request(url, headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"})
        form_data = {'detail': '0', 'plat': str(platform), 'queryString': '', 'sortd': 'Normal Order', 'sorthead': 'popular', 't': 'games'}
        params = urllib.parse.urlencode(form_data).encode("utf-8")
        html = urllib.request.urlopen(request, params).read()

        # print(html)
        root = lxml.html.fromstring(html)


        expected_end_marker = root.xpath("//li/text()")
        print("bla: " + expected_end_marker[0])
        if "No results" in expected_end_marker[0]:
            print("final page for " + platform + " reached")
            break

        # No, not done yet. Continue with products
        products = root.xpath("//li")

        print(len(products))

        for product in products:
            data = {}

            data['title'] = str(product.xpath("div[2]/h3/a/text()")[0])


            main_story_length = product.xpath("div[2]/div/div[1]/div[2]/text()")
            if len(main_story_length) == 0 or main_story_length[0] == '--':
                data['main_story_length'] = ''
            else:
                data['main_story_length'] = str(main_story_length[0])

            mainextra_length = product.xpath("div[2]/div/div[2]/div[2]/text()")
            if len(mainextra_length) == 0 or mainextra_length[0] == '--':
                data['mainextra_length'] = ''
            else:
                data['mainextra_length'] = str(mainextra_length[0])

            completionist_length = product.xpath("div[2]/div/div[3]/div[2]/text()")
            if len(completionist_length) == 0 or completionist_length[0] == '--':
                data['completionist_length'] = ''
            else:
                data['completionist_length'] = str(completionist_length[0])

            combined_length = product.xpath("div[2]/div/div[4]/div[2]/text()")
            if len(combined_length) == 0 or combined_length[0] == '--':
                data['combined_length'] = ''
            else:
                data['combined_length'] = str(combined_length[0])

            data['platform'] = platform

            # print(data)

            csv_writer.writerow(data)

        # Do the next page of results
        page += 1

