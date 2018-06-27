import re
import csv
import os
from tools import csv2dictlist, get_fname_sewolho
import argparse


def clean_text(text: str):
    # list like str to str
    cleaned_text = re.sub(r'\[\'|\', \'|\'\]', ' ', text)

    # delete html tag
    cleaned_text = re.sub(r'<!--.*-->', r' \\n ', cleaned_text)
    cleaned_text = re.sub(r'\\xa0|\\uf0a0|\\uf0a7|\\uf09f|\\u3000|\\ufeff', r' \\n ', cleaned_text)

    # make new line
    cleaned_text = re.sub(r'\\t|\\r|\\n|\.', r' \\n ', cleaned_text)
    cleaned_text = re.sub(r'(\\n *)+', r' \\n ', cleaned_text)

    # delete special characters leave only hangle, alphabet, numbers
    # delete not complete hangle also. For example, ㅌ, ㄴ, ...
    cleaned_text = re.sub(r'[^가-힣a-zA-Z1-9|\\n]', ' ', cleaned_text)
    cleaned_text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ]', ' ', cleaned_text)

    # need: delete reporter and email and return

    # delete duplicate space
    cleaned_text = re.sub(r' +', ' ', cleaned_text)

    # trim whitespace
    cleaned_text = cleaned_text.strip()

    return cleaned_text


def get_cleantexts(fname: str):
    news = csv2dictlist(fname)
    clean_texts = [line['clean_text'] for line in news]
    return clean_texts


def get_texts(fname: str):
    news = csv2dictlist(fname)
    texts = [line['text'] for line in news]
    return texts


def save_clean_text(press: str, dirname: str, out_dirname: str):
    # get file name
    fname = get_fname_sewolho(press, dirname)

    # open file and get dict list
    total_news = csv2dictlist(fname)

    # execute clean text
    for news in total_news:
        news['clean_text'] = clean_text(news['text'])

    # determine output file name
    out_fname = fname.split('/')[-1]
    out_fname = out_fname.replace('.csv', '_clean.csv')
    out_fname = os.path.join(out_dirname, out_fname)
    if not os.path.isdir(out_dirname):
        os.makedirs(out_dirname)

    # save to out_fname
    with open(out_fname, 'w', newline='', encoding='utf-8-sig') as csvoutput:
        writer = csv.DictWriter(csvoutput, fieldnames=total_news[0].keys())
        writer.writeheader()
        writer.writerows(total_news)
        print('saved to [' + out_fname + ']')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--press', type=str, default='더불어민주당')
    args.add_argument('--dir', type=str, default='sewolho')
    args.add_argument('--out_dir', type=str, default='clean_text')

    config = args.parse_args()
    save_clean_text(config.press, config.dir, config.out_dir)
