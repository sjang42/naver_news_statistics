import csv
import os


def csv2dictlist(fname):
    """Read a csv file and convert it to list of dictionary
    :param fname: (str) file name
    :return: list of dictionary
    """
    with open(fname, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, skipinitialspace=True)
        header = next(reader)
        dictlist = [dict(zip(header, row)) for row in reader]

    return dictlist


def list_to_str(lst):
    ret = ''
    for a in lst:
        if a != lst[0]:
            ret += '_'
        ret += a

    return ret


def get_fname(query,
              press,
              period_from,
              period_to,
              pages_from,
              pages_to,
              ext,
              is_enumerate=False):
    press_str = list_to_str(press)
    if not is_enumerate:
        fname = query + '_' + period_from + 'to' + period_to + '_p' + str(
            pages_from) + '-p' + str(pages_to) + '_' + press_str + '.' + ext
    else:
        fname = query + '_enum_' + period_from + 'to' + period_to + '_' + press_str + '.' + ext
    return fname


def get_fname_sewolho(press: str, dirname=None):
    """Get file name of sewolho news that is released from press"""
    if type(press) != list:
        press_list = [press]
    else:
        press_list = press

    fname_sewolho = get_fname(
        query='세월호',
        press=press_list,
        period_from='2014.04.16',
        period_to='2015.04.11',
        pages_from=None,
        pages_to=None,
        ext='csv',
        is_enumerate=True)
    if dirname:
        fname_sewolho = os.path.join(dirname, fname_sewolho)

    return fname_sewolho
