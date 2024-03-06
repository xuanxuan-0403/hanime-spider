import requests
import re
import os
import json
import xml.etree.ElementTree as ET

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/118.0.0.0 Safari/537.36'
}


# 获取第一集的信息
def getTvInfo(path: str, videoArr: list[str]):
    info = {
        "title": '',  # 原标题
        "artistName": '',  # 艺术家
        "captionText": '',  # 简介
        "updateTime": '',  # 更新日期
        "tags": []
    }
    r = requests.get(url=videoArr[-1], headers=headers)
    if r.status_code == 200:
        title = re.compile(r'shareBtn-title.*?>(?P<title>.*?)</h3>').search(r.text).group('title')
        info['title'] = title
        artistName = re.compile(r'<a id="video-artist-name".*?>(?P<artistName>.*?)</a>', re.S).search(r.text).group(
            'artistName')
        info["artistName"] = artistName.lstrip().rstrip()
        captionText = re.compile(r'<div class="video-caption-text.*?>(?P<captionText>.*?)</div>', re.S).search(
            r.text).group('captionText')
        info["captionText"] = captionText
        updateTime = re.compile(r'觀看次數.*?&nbsp;&nbsp;(?P<updateTime>.*?)</div>').search(r.text).group('updateTime')
        info["updateTime"] = updateTime
        tags_regex = re.compile(
            r'<div class="single-video-tag" style="margin-bottom: 18px; font-weight: normal">.*?>(?P<tag>.*?)</a></div>',
            re.S)
        for tag in tags_regex.finditer(r.text):
            info["tags"].append(tag.group('tag'))

        r.close()
        print(info)
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(info, json_file, ensure_ascii=False)

        # 创建 XML 元素
        root = ET.Element("tvshow")
        outline = ET.SubElement(root, "outline").text = info['title']
        # 创建 ElementTree 对象
        tree = ET.ElementTree(root)
        # 保存到 NFO 文件
        nfo_file_path = "movie.nfo"
        tree.write(nfo_file_path, encoding='utf-8', xml_declaration=True)

        return info


if __name__ == '__main__':
    getTvInfo('test.json', ['https://hanime1.me/watch?v=13007'])
