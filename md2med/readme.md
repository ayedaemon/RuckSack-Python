>> A simple script to upload my hugo markdown pages to medium.

#### How to use?

1. Create a `.md` file for the blog (see the demo file `./article/article.md`)

2. Create a file with name `token` in the same directory as `app.py`. And paste your medium integration token in that file.

3. Run `app.py` and pass the path of the article to be uploaded.

```
python3 app.py ./article/article.md
```

This will upload the article to medium.


#### To-Do
- Add feature to handle local images
- make a better config file.
- Better error handling and useful messages
