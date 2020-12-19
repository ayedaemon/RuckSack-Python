from core import (MediumPost, IO)

input_path = 'posts/'
output_path = 'converted_posts/'


if __name__ == '__main__':
    ## Get all the posts files in the folder
    posts = IO(input_path, 'read')

    ## Get data of a single post
    for i, post_path in enumerate(posts):
        with open(post_path) as f:
            html = f.read()

        m = MediumPost(html)
        m.get_subtitle()
        m.get_heading()
        m.get_kicker()
        m.get_body()

        ## Write to the .md file
        IO(output_path+post_path, 'write', m.payload)
        print(f"[ {i+1} - DONE ]  {m.payload.get('heading','-')}")
        # print(m.payload.get('heading','-'))
        # print(m.payload.get('kicker','-'))
