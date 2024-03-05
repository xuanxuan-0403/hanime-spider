import requests
import re
import os
from tqdm import tqdm


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
