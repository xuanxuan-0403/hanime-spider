from utils.get_TV_info import getTvInfo
from utils.index import getSearchData, getFirstPageData, handleDownloadAudio
from utils.audio_downloader import downloadAudio

if __name__ == '__main__':
    name = input('输入你要查询的番剧名: ')
    search_hrefs: list[str] = getSearchData(name)  # 根据番剧名抓取所有剧集 href
    # getTvInfo('assets/test.json', search_hrefs)  # 元信息
    download_page_href: list[str] = getFirstPageData(search_hrefs)  # 抓取剧集内下载按钮的下载链接
    infos, download_url = handleDownloadAudio(download_page_href)
    print(infos, download_url)
    for info in infos:
        downloadAudio(name, info['title'], info['url'])
