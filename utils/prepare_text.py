import re
import pandas as pd


# return True if string is code with unread symbols or too long to read
def substring_is_code(string):
    string_ = re.sub(r'\s+', '', string)
    return not (string_.isalnum() and len(string) < 50)


# replacing characters with their names
def replace_symbols_for_latex(string):
    symb_dict = dict({
        '+': ' plus ',
        '-': ' minus ',
        '*': ' multiply ',  # сonvolution?
        '/': ' divide ',
        '=': ' equals ',
        '<': ' less than ',
        '>': ' greater than ',
        '&': ' and ',
        # '|': ' or ', module?
        '~': ' not ',
        '!': ' not ',
        '%': ' mod ',
        '^': ' pow ',
        "'": ' with accent '
    })
    res = string
    for symb in string:
        if symb in symb_dict.keys():
            res = res.replace(symb, symb_dict[symb])
    return res


def replace_symbols_for_code(string):
    symb_dict = dict({
        '+': 'plus',
        '-': 'minus',
        '*': 'star',
        '/': 'slash',
        '\\': 'backslash',
        '=': 'equals',
        '<': 'less than',
        '>': 'greater than',
        '&': 'ampersand',
        '@': 'at',
        '~': 'tilde',
        '%': 'percent',
        '.': 'dot',
    })
    res = string
    for symb in string:
        if symb in symb_dict.keys():
            res = res.replace(symb, symb_dict[symb])
    return res


# find text between <start_string> and <end_string> and replace with replace_function
# if start_string_end is not None, then <start_string> is '<start_string>...<start_string_end>'
# start_string_end is for spacial case '<code class= ... > ... </code>'
def find_and_replace(string, start_string, end_string, replace_function, start_string_end=None):
    ind_start = string.find(start_string)
    while ind_start != -1:
        ind_end = string.find(end_string, ind_start)
        if start_string_end is None:
            ind_start += len(start_string)
        else:
            ind_start = string.find(start_string_end, ind_start) + len(start_string_end)

        substring = string[ind_start:ind_end]

        new_substring = replace_function(substring)

        string = string[
                 :ind_start - (0 if start_string_end else len(start_string))] + ' ' + new_substring + ' ' + string[
                                                                                                            ind_end + len(
                                                                                                                end_string):]
        ind_end -= (len(substring) + len(end_string) + len(start_string)) - (2 + len(new_substring))

        ind_start = string.find(start_string, ind_end)
    return string


def clean_latex(string):
    # delete \ ( )
    res = re.sub(r'\\', '', string)
    res = re.sub(r'\(|\)', ' ', res)

    # delete quad
    res = res.replace('quad', ' ')

    # split subindex to different symbols:
    # e_{12} -> e 1 2
    # e_{2n} -> e 2 n
    def replace_function(string_):
        return ' '.join(string_)

    res = find_and_replace(res, '_{', '}', replace_function)

    # replace ⋅ as dot
    res = re.sub(r'cdot', 'dot', res)
    # replace ldots, vdots
    res = re.sub(r'ldots|vdots', ' dots ', res)
    # add spaces near ' ^
    res = re.sub(r"'", " ' ", res)
    res = re.sub(r'\^', ' ^ ', res)
    # replace <= and >=
    res = re.sub(r'leq|le', ' less or equals than ', res)
    res = re.sub(r'geq|ge', ' greater or equals than ', res)

    # replace \ne, \neq
    res = re.sub(r'neq|ne', ' not equals ', res)

    # replace \longrightarrow and \leadsto and \to
    res = re.sub(r'longrightarrow', ' goes to ', res)
    res = re.sub(r'leadsto', ' goes to ', res)
    res = re.sub(r'to', ' goes to ', res)
    # res = re.sub(r'rightleftarrows', ' not equals ', res) # replace for what?

    # replace '\right(' and '\left(' to '(' and ')'
    res = re.sub(r'right\)', ')', res)
    res = re.sub(r'left\(', '(', res)

    # delete all matrix
    # begin{pmatrix} .. end{pmatrix} -> matrix
    def replace_function(string_):
        return 'matrix'

    res = find_and_replace(res, 'begin{pmatrix}', 'end{pmatrix}', replace_function)

    # replace frac{}{}
    # frac{a}{b} -> a / b
    ind_start_a = res.find('frac{')
    while ind_start_a != -1:
        ind_start_a += len('frac{')
        ind_end_a = res.find('}', ind_start_a)
        A = res[ind_start_a:ind_end_a]
        len_a = len(A)

        ind_start_b = res.find('{', ind_start_a)
        ind_start_b += len('{')
        ind_end_b = res.find('}', ind_start_b)
        B = res[ind_start_b:ind_end_b]
        len_b = len(B)

        res = res[:ind_start_a - len('frac{')] + A + ' / ' + B + res[ind_end_b + len('}'):]
        ind_end_b = ind_end_b - len('frac{}{}') + len(' / ')
        ind_start_a = res.find('frac{', ind_end_b)

    # delete \\mathbf, mathbb
    res = re.sub(r'mathbf|mathbb', '', res)

    # delete \text
    res = re.sub(r'text', '', res)

    # delete { } _
    res = re.sub(r'{|}|_', ' ', res)

    # replace ^* as 'with star'
    # e^* -> e with star
    # like e' -> e with accent
    res = re.sub(r'\^\s+\*', ' with star ', res)

    # replace symbols
    res = replace_symbols_for_latex(res)

    # delete '  '
    res = re.sub(r'\s+', ' ', res)

    return res


# split sentences if len > 200 symbols
def separate_sentences(text, max_len=200):
    sentences = text.split('.')
    for ind, sent in enumerate(sentences):
        start = 0
        while start < len(sent) - max_len:
            end = sent[start:start+max_len].rfind(',')
            if end == -1:
                end = sent[start:start+max_len].rfind(' ')
            sent = sent[:end] + '. ' + sent[end+1:].lstrip().capitalize()
            start = end + 1
        sentences[ind] = sent
    return '.'.join(sentences)


# INPUT : sample: str
def prepare_sample(sample):
    # try to delete code-style text, see 'substring_is_code' function
    def replace_function(string_):
        string = replace_symbols_for_code(string_)
        if substring_is_code(string):
            return ''
        else:
            return string

    sample = find_and_replace(sample, '<code class=', '</code>', replace_function, '>')

    # delete math-tex, see clean_latex
    sample = find_and_replace(sample, '<span class=\\"math-tex\\">', '</span>', clean_latex)

    # delete html
    sample = re.sub(r'\<[^>]*\>', '', sample)
    # delete \n, \t, \\
    sample = re.sub(r'\n|\\n|\\t|\\', ' ', sample)
    # delete first, last "
    if sample[0] == '"':
        sample = sample[1:]
    if sample[-1] == '"':
        sample = sample[:-1]
    # delete '  '
    sample = re.sub(r'\s+', ' ', sample)

    sample = separate_sentences(sample)

    return sample


def save_sample_to_file(sample, path='samples/new_sample.txt'):
    f = open(path, 'w', encoding='utf-8')
    f.write(sample)
    f.close()


# get samples from csv, prepare and put to path_to_samples/
def prepare_and_save_samples_from_csv(csv_name, path_to_samples_dir='samples/'):
    data = pd.read_csv(csv_name)['text']

    samples = []
    for ind_d, d in enumerate(data):
        samples.append(prepare_sample(d))

    for i, sample in enumerate(samples):
        save_sample_to_file(sample, path_to_samples_dir + f'sample{i}.txt')
