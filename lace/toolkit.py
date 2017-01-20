from __future__ import division
from bisect import bisect_left
from stat_helper import a12s as a12rank
import bins
import csv

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


def str2num(s):
    if type(s) == float or type(s) == int: return s
    try:
        s = int(s)
    except ValueError:
        try:
            s = float(s)
        except ValueError:
            pass
    return s


def median(l):
    """
    return the median of the list l.
    l WILL NOT be changed.
    :param l:
    :return:
    >>> median([4,2,2,2,1,1,1,1,1,1,1,1,1])
    1
    """
    return sorted(l)[int(len(l)/2)]


def binrange(data_list, enough=None, cohen=0.2, maxBins=16, minBin=4, trivial=1.05):
    """

    :param data_list:
    :param enough:
    :param cohen:
    :param maxBins:
    :param minBin:
    :param trivial:
    :return: ist of bin# e.g. {a,b,c,d,e} [a,b] (b,c] (c,d] (d,e]
    """
    ranges = bins.bins(t=data_list, enough=enough, cohen=cohen,
                       maxBins=maxBins, minBin=minBin,trivial=trivial)
    res = [ranges[0].lo]
    for r in ranges:
        res.append(r.up)
    return res


def apply_bin_range(datalist, enough=None, cohen=0.2, maxBins=16, minBin=4, trivial=1.05):
    if len(datalist) == 0: return datalist
    range_divide = binrange(datalist, enough, cohen, maxBins, minBin, trivial)
    x = list()
    for i in datalist:
        t = bisect_left(range_divide, i)
        x.append(t)
    return x


def attr_norm(all_elements):
    """
    This is the normalization/de-normalization function generator for one kind of attribute
    :param all_elements: all the elements for one attribute
    :return: two functions. The first one can normalize the element; the second one is de-normalize the element

    e.g.
    loc = [100,200,100,300]
    norm_loc, denorm_loc = attr_norm(loc)
    l1 = map(norm_loc,loc)
    l2 = map(denorm_loc, l1)
    print l1 # [0.0, 0.5, 0.0, 1.0]
    print l2 # [100.0, 200.0, 100.0, 300.0]
    """
    if not type(all_elements) is list: all_elements = [all_elements]
    M = max(all_elements)
    m = min(all_elements)

    def norm(element):
        return (element-m)/(M-m) if M != m else 1

    def denorm(element):
        s = element*(M-m)+m if M != m else m
        if m <= s <= M:
            return s
        elif m < s:
            s = 2 * m - s
        else:
            s = 2 * M - s
        return max(min(s, M), m)

    return norm, denorm


def euclidean_dist(x, y):
    """
    the Eulerian distance between x and y
    :param x: instance x. type--list or one number
    :param y: instance y. type--list or one number
    :return: the Eulerian distance between x and y
    """
    if type(x) is not list:
        x = [x]
    if type(y) is not list:
        y = [y]

    assert len(x) == len(y), "the dimension of two parameters must be the same"

    return sum([(i-j)**2 for i, j in zip(x, y)]) ** 0.5


def normalize_cols_for_table(table):
    """
    normalize a list of list--table
    data are grouped by cols
    :param table:
    :return:
    """
    result = []
    for col in zip(*table):
        f1, f2 = attr_norm(list(col))
        result.append(map(f1, col))
    return map(list, zip(*result))


def del_col_in_table(list_of_list, col_index):
    """
    delete one column or multiple columns in the table (list of list)
    :param list_of_list: data table
    :param col_index: index of the col. can be single number or a list. can be negative
    :return: new alloc pruned table
    """

    if type(col_index) is not list:
        col_index = [col_index]
    for i in range(len(col_index)):
        if col_index[i] < 0:
            col_index[i] += len(list_of_list[0])

    list_of_list = map(list, zip(*list_of_list))
    return_table = []
    for index, col in enumerate(list_of_list):
        if index not in col_index:
            return_table.append(col)
    return map(list, zip(*return_table))


def load_csv(folder, file_name, has_header=True):
    """
    loading the csv file at folder/file_name.csv
    :param folder:
    :param file_name:
    :param has_header:
    :return: (header if possible) + (content)
    """
    if not folder.endswith('/'):
        folder += '/'
    folder = folder.replace('//', '/')

    with open(folder + file_name+'.csv', 'r') as db:
        reader = csv.reader(db)
        if has_header:
            header = next(reader)
        content = []
        for line in reader:
            content.append(line)
    if has_header:
        return header, content
    else:
        return content


def write_csv(folder, file_name, content, header=None):
    with open(folder + '/' + file_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        writer.writerows(content)


def append_csv_row(folder, file_name, row):
    with open(folder+'/'+file_name+'.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def log_v(variable, value):
    if type(value) is str:
        print(variable + ": " + value)
    else:
        print(variable + ": " + str(value))


def make_it_list(single_object_or_a_list):
    if type(single_object_or_a_list) is not list:
        single_object_or_a_list = [single_object_or_a_list]
    return single_object_or_a_list


def a12s(rxs,rev=False,enough=0.75):
    """
     Given a performance measure M seen in m measures of X and n measures
; of Y, the A12 statistics measures the probability that running
; algorithm X yields higher M values than running another algorithm Y.
;
; A12 = #(X > Y)/mn + 0.5*#(X=Y)/mn
;
; According to Vargha and Delaney, a small, medium, large difference
; between two populations:
;
; + Big is A12 over 0.71
; + Medium is A12 over 0.64
; + Small is A12 over 0.56
;
; In my view, this seems gratitiously different to...
;
; + Big is A12 over three-quarters (0.75)
; + Medium is A12 over two-thirds (0.66)
; + Small is A12 over half (0.5)
;
; Whatever, the following code parameterizes that magic number
; so you can use the standard values if you want to.
;
; While A12 studies two treatments. LA12 handles multiple treatments.
; Samples from each population are sorted by their mean. Then
; b4= sample[i] and after= sample[i+1] and rank(after) = 1+rank(b4)
; if a12 reports that the two populations are different.

To simplify that process, I offer the following syntax. A population
; is a list of numbers, which may be unsorted, and starts with some
; symbol or string describing the population. A12s expects a list of
; such populations. For examples of that syntax, see the following use cases

rxs= [["x1", 0.34, 0.49, 0.51, 0.60],
["x2", 0.9, 0.7, 0.8, 0.60],
["x3", 0.15, 0.25, 0.4, 0.35],
["x4", 0.6, 0.7, 0.8, 0.90],
["x5", 0.1, 0.2, 0.3, 0.40]]
for rx in a12s(rxs,rev=False,enough=0.75): print rx
    """

    return a12rank(rxs, rev, enough)
