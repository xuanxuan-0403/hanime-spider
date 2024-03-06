from setuptools import setup, find_packages

setup(
    name='xr-hanime-spider',
    version='0.1.0',
    author='xuanxuan-0403',
    author_email='1302030435@qq.com',
    url='https://github.com/xuanxuan-0403',
    description='Hanime 网站爬虫，可以批量下载查询的番剧，等其他功能',
    packages=find_packages(),
    install_requires=[
        'json',
        're',
        'os',
        'requests',
        'ET',
        'tqdm'
    ]
)
