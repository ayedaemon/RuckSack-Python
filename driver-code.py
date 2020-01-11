#!/usr/bin/python3.6

import mailer.mailer as mailer


def get_file():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", help="path of the file containing the emails.")
    parser.add_argument("--filetype", help="type of the file",  choices=['text','csv'])
    args = parser.parse_args()
    return (args.filepath, args.filetype)

if __name__ == '__main__':
    m = mailer.Mailer()
    filepath, filetype = get_file()
    mails_gen = m.fetch_mails(filepath,filetype)
    with open("fetched-mails.txt",'w') as f:
        for mail in mails_gen:
            f.write(mail+"\n")
    print("[+] saved all mails..")
    
