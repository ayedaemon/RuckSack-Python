# med2md
> Tool to convert medium posts to markdown.


#### Steps
  - Download the medium data (from medium website). This will give you a zip file which contains a lot of your data.
  - Extract the zip. Take your posts folder and paste it here. (For eg:- `posts/` here is my posts folder)
  - Edit `med2md.py` file. Write your input and output directory.
  - Change the template accordingly. For now it only supports:
  ```
    - KICKER
    - BODY
    - TITLE
    - SUBTITLE
  ```
  - Run:- `python3 med2md.py`
