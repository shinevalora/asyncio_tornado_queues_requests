# _*_coding:utf-8_*_
#  作者    : shinevalora
#  创建时间: 2019/7/9  20:05

# _*_coding:utf-8_*_
#  创建时间: 2019/7/8  22:05


import re
import logging
import asyncio
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s: %(message)s")

headers = {'User-Agent': 'Mozilla/5.0'}




async def get_data():
    await asyncio.sleep(0)

    with open('douban_top250.txt', 'a', encoding='utf-8') as file:
        file.write('Rank,Title,Director,Actors,Year,Country,Categories,Score,Number,Comments\n')
        for page in range(0, 250, 25):
            html = requests.get(f"https://movie.douban.com/top250?start={str(page)}&filter=", headers=headers).text
            logging.info(f"page is {page}")

            pat = re.compile(
                r'<em class="">(.*?)</em>.*?<img width="100" alt="(.*?)" src=".*?" class="">.*?<p class="">(.*?)</p>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)人评价</span>.*?<span class="inq">(.*?)</span>',
                re.S)

            all_pattern = re.findall(pat, html)
            logging.info(f"len(all_pattern) is {len(all_pattern)}")

            for i in all_pattern:
                rank = i[0]
                title = i[1]
                text = i[2].replace("\n                            ", " ").replace("&nbsp;&nbsp;&nbsp;", "# #").replace(
                    "&nbsp;", "#").replace("/", " ").replace("...", " ").replace("<br>", "# #").replace(
                    "\n                        ", " ")

                contents = text.split("# #")
                director = contents[0]
                actors = contents[1]
                year = contents[2]
                country = contents[3]
                categories = contents[-1]
                score = i[3]
                number = i[4]
                comments = i[5]

                file.write(
                    rank + "," + title + "," + director + "," + actors + "," + year + "," + country + "," + categories + "," + score + "," + number + "," + comments + "\n")

                logging.info(f"rank, {rank}")
                logging.info(f"title, {title}")
                logging.info(f"director, {director}")
                logging.info(f"'actors, {actors}")
                logging.info(f"year, {year}")
                logging.info(f"country, {country}")
                logging.info(f"categories, {categories}")
                logging.info(f"score, {score}")
                logging.info(f"number, {number}")
                logging.info(f"comments, {comments}")


async def create_task():
    task1 = asyncio.create_task(get_data())

    await task1


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(create_task())
    end_time = time.time()
    logging.info(f"总共消耗的时间为： {end_time - start_time} s")
