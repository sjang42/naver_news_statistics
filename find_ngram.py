import collections
import time
import os
from tools import get_fname_sewolho
from clean_text import get_cleantexts


def tokenize(string):
    """Convert string to lowercase and split into words (ignoring
    punctuation), returning list of words.
    """
    return string.split(' ')


def count_ngrams(lines, min_length=2, max_length=4):
    """Iterate through given lines iterator (file object or list of
    lines) and return n-gram frequencies. The return value is a dict
    mapping the length of the n-gram to a collections.Counter
    object of n-gram tuple and number of times that n-gram occurred.
    Returned dict includes n-grams of length min_length to max_length.
    """
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}
    queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for line in lines:
        for word in tokenize(line):
            if word == '\\n':
                queue.clear()
                continue
            queue.append(word)
            if len(queue) >= max_length:
                add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()

    return ngrams


def print_most_frequent(ngrams, num=100):
    """Print num most common n-grams of each length in n-grams dict."""
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print('')


def save_ngram(ngrams,
               fname,
               min_count=-1,
               save_dir='./',
               min_length=1,
               max_length=3):
    lengths = range(min_length, max_length + 1)

    # determine file name to save
    out_fnames = list()
    for length in lengths:
        out_fname = fname.replace('.csv', '_' + str(length) + 'ngram')
        if min_count < 0:
            out_fname = out_fname + '_all.csv'
        else:
            out_fname = out_fname + str(min_count) + '.csv'

        out_fname = os.path.join(save_dir, out_fname)
        out_fnames.append(out_fname)

    for idx, length in enumerate(lengths):
        print('----- {} most common {}-grams -----'.format(min_count, length))
        print('saving to ... [{}]'.format(out_fnames[idx]))

        with open(out_fnames[idx], encoding='utf-8-sig', mode='w') as fp:
            fp.write(str(length) + 'gram word, frequency\n')

            for gram, count in ngrams[length].most_common():
                if min_count == -1 or count >= min_count:
                    fp.write(' '.join([str(word) for word in gram]) + ', ' +
                             str(count) + '\n')
        print('')


def get_input():
    print('''
    press : The name of press to find ngram
    dirname : Path to directory having news contents
    minimum length, maximum length: Find ngram of length from min to max
    minimum count : Only save the ngrams found more than minimum count 
    ''')
    press = input('Enter press : ')
    dirname = input('Enter directory : ')
    min_length = input('Enter minimum length of ngram : ')
    max_length = input('Enter maximum length of ngram : ')
    min_count = input('Enter minimum count of ngram (-1 for all) : ')

    return press, dirname, int(min_length), int(max_length), int(min_count)


if __name__ == '__main__':
    print('----- Count Ngram -----')
    press, dirname, min_length, max_length, min_count = get_input()

    fname = get_fname_sewolho(press, dirname)
    fname = fname.replace('.csv', '_clean.csv')

    start_time = time.time()
    clean_texts = get_cleantexts(fname)

    ngrams = count_ngrams(
        clean_texts, min_length=min_length, max_length=max_length)
    save_ngram(
        ngrams=ngrams,
        fname=fname,
        min_count=min_count,
        save_dir='ngrams',
        min_length=min_length,
        max_length=max_length)

    elapsed_time = time.time() - start_time
    print('Took {:.03f} seconds'.format(elapsed_time))
