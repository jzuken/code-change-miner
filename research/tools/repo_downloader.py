import settings
import requests
import os
import logging
import subprocess


_GITHUB_BASE_URL = 'https://api.github.com'
_REPO_DIR = settings.get('research_repo_dir', os.getcwd())
_REPO_CNT = settings.get('research_repo_count', 10)
_TOKEN = settings.get('research_github_token')


def main():
    logging.warning('Starting')

    page_num = 1
    visited_repo_cnt = 0

    while True:
        if visited_repo_cnt > _REPO_CNT:
            break

        headers = {'Authorization': f'token {_TOKEN}'} if _TOKEN else None
        r = requests.get(f'{_GITHUB_BASE_URL}/search/repositories?'
                         f'q=language:python&sort=stars&order=desc&page={page_num}&per_page=100',
                         headers=headers)
        data = r.json()
        items = data['items']

        for item in items:
            url = item['clone_url']
            args = ['git', 'clone', url]
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            p.communicate()

            logging.warning(f'Visited: {item["full_name"]}')

            visited_repo_cnt += 1
            if visited_repo_cnt > _REPO_CNT:
                break

        page_num += 1

    logging.warning('Done')


if __name__ == '__main__':
    main()