# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def mal_spider():
    results = []

    current_limit = 0

    while True:
        current_url = "https://myanimelist.net/topanime.php?limit={}".format(
            current_limit
        )

        page_content = requests.get(current_url).content
        soup_content = BeautifulSoup(page_content, "html.parser")

        current_list = soup_content.findAll("table", class_="top-ranking-table")[
            0
        ].findAll("tr", class_="ranking-list")

        for each in current_list:
            anime_name = (
                each.findAll("div", class_="detail")[0]
                .findAll("a", class_="hoverinfo_trigger")[0]
                .text
            )
            anime_score = (
                each.findAll("td", class_="score")[0]
                .findAll("span", class_="score-label")[0]
                .text
            )

            results.append({anime_name: anime_score})

        if (
            len(
                soup_content.findAll("div", class_="icon-top-ranking-page-bottom")[
                    0
                ].findAll("a", class_="next")
            )
            < 1
        ):
            break

        current_limit += 50

    return results
