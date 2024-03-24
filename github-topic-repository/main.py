from bs4 import BeautifulSoup
import requests
import json

def get_topic_page(topic):

    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15"
        }
    
    topic_name  = topic.replace(" ", "-").lower()
    topic_url = 'https://github.com/topics/' + topic_name

    response = requests.get(topic_url, headers = headers)
    if response.status_code != 200:
        raise Exception('Failed to fetch web page of : ' + topic_url)

    page = BeautifulSoup(response.content, 'lxml')

    return page


def parse_star_count(star):
    
    if star[-1] == 'k':
        return int(float(star[:-1]) * 1000)
    else:
        return int(star)
    
def repo_from_json(username, repo_name):
    print('Fetching information from {}/{}'.format(username, repo_name))

    repo_url = f'https://api.github.com/repos/{username}/{repo_name}'

    response = requests.get(repo_url)
    
    if not response.ok:
        print('Failed to fetch!')
        return {}
    page = json.loads(response.text)

    return page

def parse_repository(soup):

    main_url = 'https://github.com'

    repository = soup.find_all('h3', class_='f3 color-fg-muted text-normal lh-condensed')
    stars = soup.find_all('span', class_ = 'Counter js-social-count')

    top_topic = []

    for repo, star in zip(repository, stars):
        username = repo.find('a', class_ = 'Link').text.strip()
        repo_name = repo.find('a', class_ = 'Link text-bold wb-break-word').text.strip()
        link_repo = repo.find('a', class_ = 'Link text-bold wb-break-word')['href']
        star_repo = parse_star_count(star.text.strip())

        page_json = repo_from_json(username, repo_name)
        
        top_repository = {
            'repo name' : repo_name,
            'username' : username,
            'stars' : star_repo,
            'watchers' : page_json['watchers_count'],
            'created at' : page_json['created_at'],
            'updated at' : page_json['updated_at'],
            'link repo' : main_url + link_repo
        }

        top_topic.append(top_repository)

    return top_topic

def write_csv(items, path):

    with open(path, 'w') as f:
        if len(items) == 0:
            return
        
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')

        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + '\n')

def scrape_topic_repository(topic, path=None):

    if path is None:
        path = topic + '.csv'
    
    page = get_topic_page(topic)
    top_topic = parse_repository(page)
    write_csv(top_topic, path)

    print("Top repositories for topic {} written to file {}".format(topic, path))

topic = input("What topic do you want to scrape ? ")
scrape_topic_repository(topic)