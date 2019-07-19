# _*_coding:utf-8_*_
#  创建时间: 2019/7/8  22:05


import re
import logging
import asyncio
import time

from tornado import queues, httpclient

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s: %(message)s")

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = f'https://movie.douban.com/top250'
q = None
urls = set()
html = ""


file = open('douban_top250_test.txt', 'a', encoding='utf-8')
file.write('Rank,Title,Director,Actors,Year,Country,Categories,Score,Number,Comments\n')


async def get_data():
    pat = re.compile(
        r'<em class="">(.*?)</em>.*?<img width="100" alt="(.*?)" src=".*?" class="">.*?<p class="">(.*?)</p>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)人评价</span>.*?<span class="inq">(.*?)</span>',
        re.S)


    print(q)
    async for url in q:
        print(url)
        if url is None:
            return
        try:
            logging.info(f"正在抓取  {url} 页面")

            response = await httpclient.AsyncHTTPClient().fetch(url)
            html = response.body.decode('utf-8')
            logging.info(f"html is  {html}")

            for a in range(25, 250, 25):
                url = base_url + f"?start={a}&filter="
                if url not in urls:
                    urls.add(url)
                    await q.put(url)

            all_pattern = re.findall(pat, html)
            logging.info(f"len(all_pattern) is {len(all_pattern)}")

            for i in all_pattern:
                rank = i[0]
                title = i[1]
                text = i[2].replace("\n                            ", " ").replace("&nbsp;&nbsp;&nbsp;",
                                                                                   "# #").replace(
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

            q.task_done()

        except Exception as e:
            logging.info(f"报错原因是  {e}")
            raise e



async def main():
    global q
    q = queues.Queue()

    await q.put(base_url)

    task_lists = [asyncio.create_task(get_data()) for i in range(10)]

    # logging.info(f"task_list is {task_lists}")

    await q.join()

    for _ in task_lists:
        await q.put(None)


if __name__ == '__main__':
    start_time = time.time()

    asyncio.run(main())

    end_time = time.time()



    logging.info(f"总共消耗的时间为： {end_time - start_time} s")
