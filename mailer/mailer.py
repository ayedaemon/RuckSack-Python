#!/usr/bin/python3.6



class Mailer:
    def __init__(self):
        print("Welcome to Mass Mailer")

    def grep_mail_from_junk(self, text):
        import re
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        for w in text.split():
            if re.match(pattern, w):
                yield(w)


    def fetch_mails(self, filepath, filetype):
        print("[ ] Starting looking in {}".format(filepath))
        ## read files and create paragraph
        bulktext = ''
        if filetype == 'text':
            with open(filepath) as f:
                bulktext = f.read()
        elif filetype == 'csv':
            import pandas as pd
            df = pd.read_csv(filepath)
            bulktext = " ".join([" ".join(df[column].values) for column in list(df)])

        ## send paragraph to grep mails
        return self.grep_mail_from_junk(bulktext)
