from konlpy.tag import Kkma, Mecab, Twitter, Komoran


# delete not needed tags
def trim_word(word: str, tagger):
    tokenized_word = tagger.pos(word)
    trimed_word = ''
    tags_to_remove = []

    # remove from Mecab
    # tags_to_remove += ['JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JX', 'EP', 'EF', 'EC']

    # remove from Twitter
    # tags_to_remove += ['Josa', 'PreEomi', 'Eomi', 'Conjunction', 'Suffix']

    # remove from Kkma
    tags_to_remove += ['EPH', 'EPT', 'EPP', 'EFN', 'EFQ', 'EFO', 'EFA', 'EFI', 'EFR', 'ECE', 'ECS', 'ECD', 'ETN', 'ETD']
    tags_to_remove += ['JKS', 'JKC', 'JKG', 'JKO', 'JKM', 'JKI', 'JKQ', 'JC', 'JX']
    for (text, tag) in tokenized_word:
        if tag not in tags_to_remove:
            trimed_word += text

    return trimed_word
