import re
import os

def IO(path, action='read', payload=None):
    posts = []
    if action == 'read':
        for root, directories, files in os.walk(path, topdown=False):
        	for name in files:
        		posts.append(os.path.join(root, name))
        print(f"[ + ] Total posts: {len(posts)}")
        return posts
    elif action == 'write':
        with open('template.md') as f:
            template = f.read()
            template = template.replace("{{KICKER}}", payload.get('kicker','-'))
            template = template.replace("{{TITLE}}", payload.get('heading','-'))
            template = template.replace("{{SUBTITLE}}", payload.get('subtitle','-'))
            template = template.replace("{{BODY}}", payload.get('body','-'))
        blogname = path.split('/')[-1].split('_')[-1]
        try:
            os.mkdir('/'.join(path.split('/')[:-1]))
        except FileExistsError as err:
            pass
        except Exception as ex:
            print('[ - ] ',ex)

        blogname = '-'.join(blogname.split('-')[:-1])+'.md'
        op_path = '/'.join(path.split('/')[0:-1]+[blogname])
        with open(op_path, "w") as f:
            f.write(template)
    else:
        print('[ - ] {action} not defined!! ')


class MediumPost():
    def __init__(self, html):
        self.html = html
        self.payload = {}


    def get_heading(self):
        pattern = '<h1 class="p-name">(.*?)</h1>'
        heading = re.findall(pattern, self.html)[0]
        self.payload['heading'] = heading

    def get_kicker(self):
        pattern = '<h4 .*?--kicker">(.*?)<\/h4>'
        kicker = re.findall(pattern, self.html)
        if kicker:
            self.payload['kicker'] = kicker[0]

    def get_subtitle(self):
        pattern = '''<section data-field="subtitle" class="p-summary">
(.*?)
<\/section>'''
        subtitle = re.findall(pattern, self.html)[0]
        self.payload['subtitle'] = subtitle

    def get_body(self):
        pattern = '.*title">.*?<.*?>(.*)<\/section>'
        body = re.findall(pattern, self.html)[0]
        from markdownify import markdownify
        md = markdownify(body)
        self.payload['body'] = md
