def _request(method, path, access_token, json=None, form_data=None, files=None):
    import requests
    url = BASE_PATH + path
    headers = {
        "Accept": "application/json",
        "Accept-Charset": "utf-8",
        "Authorization": "Bearer %s" % access_token,
    }

    resp = requests.request(method, url, json=json, data=form_data,
                            files=files, headers=headers)
    return resp

def read_file(filepath, type="article"):
    with open(filepath) as f:
        data = f.read()
    print(f"[ * ] Read {len(data)} characters from {filepath}\n")

    def split_up():
        nonlocal data
        data = data.split("---")
        import yaml
        header = yaml.load(data[1], Loader=yaml.FullLoader)
        article = data[2:]
        return header,'---'.join(article)
    if type=="token":
        return data.strip()
    else:
        return split_up()


def format_article(header, article):
    article = article.split("<!--more-->")
    content = f"\n# {header['title']} \n### {article[0].strip()} \n{article[1].strip()}"
    data = {}
    if header.get('kicker'):
        content = f"### {' | '.join(header['kicker'])}" + content
    if header['tags']:
            data["tags"] = header['tags']
    if header['draft'] == True:
        data["publishStatus"] = "draft"


    data["canonicalUrl"] = "https://ayedaemon.github.io/posts/others/debugging-c-code/index.html"
    data['title'] = header['title']
    data['contentFormat'] = "markdown" ## or html
    data['content'] = content
    return data


def print_details(payload, url):
    print("\n\n***** Details *****\n")
    print(f"Uploaded to '{url}'\n")
    for k,v in payload.items():
        try:
            if len(v)>200:
                v = v[:150]+'...'
        except:
            pass
        print(f"{k:<15} -->  {v}")
    print()


def main():
    ## Get filename from the command line
    try:
        import sys
        FILEPATH = sys.argv[1]
    except IndexError:
        exit(f"Usage: python3 {sys.argv[0]} Path/to/article.md\n")
    except Exception as ex:
        print("Error: "+ex)

    ## Read file and try to split it
    try:
        header, article = read_file(FILEPATH)
    except FileNotFoundError:
        exit(f"[ - ] File '{FILEPATH}' not found!!\n")

    try: ## to read token and verify it
        TOKENFILE = "token"
        TOKEN = read_file(TOKENFILE, "token")
        print(f"[ + ] Got token - {TOKEN[:5] + '*'*len(TOKEN[5:-5]) + TOKEN[-5:]}")
        api_me = "/v1/me"
        resp = _request("GET", api_me, TOKEN)
        if resp.status_code != 200:
            exit("[ - ] Unable to get user id")
        user_id = resp.json().get('data').get('id')
        print(f"[ + ] Got User Id - {user_id}")
    except Exception as ex:
        print(ex)

    ## Post the article with usefull headers
    try:
        payload = format_article(header, article)
        path = "/v1/users/%s/posts" % user_id
        resp = _request("POST", path, json=payload, access_token=TOKEN)
        url = resp.json().get('data').get('url')
    except Exception as ex:
        print(ex)

    ## Print all details
    print_details(payload,url)

if __name__ == '__main__':
    BASE_PATH = "https://api.medium.com"
    main()
