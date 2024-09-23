import requests
import re
import os
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/118.0.0.0 Safari/537.36'
}


def getSearchData(name: str):
    main_url = 'https://hanime1.me/playlists'
    search_url = 'https://hanime1.me/search'

    params = {
        "query": name,
        "type": "",
        "genre": "",
        "sort": "",
        "year": "",
        "month": "",
    }
    search_resp = requests.get(url=search_url, headers=headers, params=params)
    if search_resp.status_code == 200:
        search_regex = re.compile(
            f'overlay.*?href="(?P<href>.*?)"',
            re.S)
        hrefs = []
        for href in search_regex.finditer(search_resp.text):
            hrefs.append(href.group('href'))
        search_resp.close()
        return list(set(hrefs))  # 数组查重


def getFirstPageData(hrefs: list[str]):
    print(hrefs)
    download_page_hrefs = []
    for href in hrefs:
        page_resp = requests.get(url=href, headers=headers)
        if page_resp.status_code == 200:
            download_regex = re.compile(f'儲存.*?<a href="(?P<href>.*?)".*?download</i>下載', re.S)
            page_result = download_regex.search(page_resp.text)
            page_href = page_result.group('href')
            download_page_hrefs.append(page_href)
            page_resp.close()

    return download_page_hrefs


def handleDownloadAudio(hrefs: list[str]):
    print(hrefs)
    download_urls = []
    info = []
    for href in hrefs:
        download_resp = requests.get(url=href, headers=headers)
        if download_resp.status_code == 200:
            download_regex = re.compile(f'play_circle_filled.*?href="(?P<href>.*?)"', re.S)
            info_title_regex = re.compile(f'download="(?P<title>.*?)"')
            download_result = download_regex.search(download_resp.text)
            download_href = download_result.group('href')
            info_title_result = info_title_regex.search(download_resp.text)
            info_title = info_title_result.group('title')
            download_urls.append(download_href)
            info.append({'title': info_title, 'url': download_href})
            download_resp.close()

    return info, download_urls


def downloadAudio(name: str, path_name: str, url: str):
    try:
        # 确保目标文件夹存在，如果不存在则创建它
        target_folder = f'./assets/{name}'
        os.makedirs(target_folder, exist_ok=True)

        response = requests.get(url, stream=True, timeout=60)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1KB
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        with open(f"./assets/{name}/{path_name}.mp4", 'wb') as file:
            for data in response.iter_content(chunk_size=block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    except Exception as e:
        print(f'下载失败:{e}')



if __name__ == '__main__':
    name = input('输入你要查询的番剧名: ')
    search_hrefs: list[str] = getSearchData(name)  # 根据番剧名抓取所有剧集 href
    download_page_href: list[str] = getFirstPageData(search_hrefs)  # 抓取剧集内下载按钮的下载链接
    infos, download_url = handleDownloadAudio(download_page_href)
    print(infos, download_url)
    for info in infos:
        downloadAudio(name, info['title'], info['url'])
