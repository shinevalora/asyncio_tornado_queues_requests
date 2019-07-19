import asyncio
import time
import logging

from lxml import etree
from tornado import httpclient, queues


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s: %(message)s")


base_url = "https://movie.douban.com/top250"

q = None



async def crawl():
    """
    根据url，获取页面内容
    根据页面内容，获取url
    :param url:
    :return: html: HTML
    """

    async for url in q:  # 获取新的目标
        if url is None:
            return  # 干掉自己
        html = ''
        try:
            print(f"正在抓取新的{url}")
            response = await httpclient.AsyncHTTPClient().fetch(url)
            html = response.body.decode()  # 字符串
            logging.info(f"type(html)   {type(html)}")
            logging.info(f" html is {html}")


        except Exception as e:
            print(f"访问出错, {e}")
            raise e
            return

        # return html

        HTML = etree.HTML(html)
        a_list = HTML.xpath('/html/body/div[3]/div[1]/div/div[1]/div[2]/a')

        for a in a_list:
            url = a.attrib['href']
            url = base_url + url  # 新的目标
            if url not in urls:  # 这个目标是否已经存在
                urls.add(url)  # 如果不存在，放入集合
                await q.put(url)  # 把新目标放入 队列
                print(url)  # 打印目标
            # await asyncio.gather(crawl())

        q.task_done()  # 告诉队列，这个任务处理完成


async def main():
    global q, urls
    q = queues.Queue()  # 异步队列，建议在协程中创建
    urls = set()

    await q.put(base_url)  # 讲起始url 放入队列
    print(11)
    task_list = [asyncio.create_task(crawl()) for i in range(20)]

    print(22)
    await q.join()

    for _ in task_list:
        await q.put(None)


if __name__ == '__main__':
    time1 = time.time()

    asyncio.run(main())

    time2 = time.time()

    print(f"一共花费了 {time2 - time1} 秒")
