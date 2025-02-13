import os
import pickle
import re

from entity_type import EntityType
from process_character.dicts import label_dict, character_dict, phrase_dict
from process_character.utils import is_cn_or_digit

VALID_CHARS = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,，。？?!！@￥*《》、【】．·-_@'


def gen_pure_data(
        input_file='process_character/data_preprocess/weiboNER_2nd_conll.',
        output_file='process_character/data_preprocess/weibo_pure_data.',
        suffixes=('train', 'test', 'dev')
):
    """
    将纵向排列的数据集横向集中，便于观察
    :param input_file:
    :param suffixes:
    :param output_file:
    :return:
    """
    #  转weiboNER_2nd_conll为相对应的weibo_pure_data
    for suffix in suffixes:
        result = []
        with open(input_file + suffix, 'r', encoding='utf-8') as f:
            current_sentence = ''
            for line in f:
                line = line.strip()  # 去除字符串首尾字符，默认是空格
                if not line:
                    result.append(current_sentence)
                    current_sentence = ''
                    continue

                char, label = line.split()
                char = char[0]
                current_sentence += char

        with open(output_file + suffix, 'w', encoding='utf-8') as f:
            i = 0
            for sentence in result:
                f.write('%s %s\n' % (i, sentence))
                i += 1

# ======================== ? for what
def rm_label_suffix(fname, only_nam=False):
    with open(fname, 'r', encoding='utf-8') as f:
        lines = []
        for line in f:
            if not line.strip():
                lines.append(line)
                continue

            char, label = line.split()
            if len(label) > 1:
                label, label_suffix = label.split('.')
                if only_nam and label_suffix != 'NAM':
                    label = 'O'
            new_line = char[0] + '	' + label + '\n'
            lines.append(new_line)

    with open(fname + '.suffix_rmed' + '_nam' if only_nam else '', 'w', encoding='utf-8') as f:
        f.writelines(lines)

# eg. 去掉weibo_pure_data中的url？
def _get_url_position_record(pure_filename):
    """
    返回准备去除url的位置
    :return:
    """
    url_pattern = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[' \
                  r'\w\-\@?^=%&/~\+#])?'

    urls_position_record = []
    with open(pure_filename, 'r', encoding='utf-8') as f:
        for line in f:
            i, text = line.split(maxsplit=1)
            i = int(i)
            urls_position_record.append({
                'number': i,
                'starts': [],
                'ends': [],
            })
            for match in re.finditer(url_pattern, text):
                urls_position_record[i]['starts'].append(match.start())
                urls_position_record[i]['ends'].append(match.end())

    return urls_position_record


def process_url(filename):
    """
    将url去除
    :return:
    """
    urls_position_record = _get_url_position_record(
        'process_character/data_preprocess/weibo_pure_data.%s' %
        filename.split('.')[-1])
    with open(filename, 'r', encoding='utf-8') as f:
        number = 0
        lines = []
        lines_of_a_sentence = []

        for line in f:
            if line.strip():
                lines_of_a_sentence.append(line)
                continue

            record = urls_position_record[number]
            starts = record['starts']
            ends = record['ends']

            if len(starts) > 0:
                for i in range(len(starts) - 1, -1, -1):
                    lines_of_a_sentence = lines_of_a_sentence[
                                          :starts[i]] + lines_of_a_sentence[ends[i]:]

            lines.extend(lines_of_a_sentence)
            lines.append('\n')
            lines_of_a_sentence = []
            number += 1

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def remove_english(filename):
    """
    去除英文字母,（去掉URL后占3.3%）
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = []

        for line in f:
            if not (line.strip() and
                    line.split()[0][0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                lines.append(line)

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def replace_rare_punctuation(filename):
    """
    将特殊符号换为comma
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = []

        for line in f:
            if not (line.strip() and
                    not is_cn_or_digit(line.split()[0]) and
                    line.split()[0] not in VALID_CHARS
            ):
                lines.append(line)
            else:
                lines.append(',' + line[1:])

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)


# raw_words, chars, char_embeddings, words, word_embeddings, pinyins, radicals, components, labels
def get_jiebaed_data(filename, outname, entity_type):
    result = []

    with open(filename, 'r', encoding='utf-8') as f:
        current_label = []
        raw_words = []
        char_index_list = []
        current_word = ''
        for line in f:
            line = line.strip()
            if line:
                char_and_index, label = line.split()
                if len(char_and_index) > 2:
                    continue

                char, index = list(char_and_index)
                index = int(index)
                if len(label) > 1:
                    label, nam_or_nom = label.split('.')
                    if entity_type == EntityType.nominal_mention:
                        label = label if nam_or_nom == 'NOM' else 'O'  # consider NAM as O
                    if entity_type == EntityType.named_entity:
                        label = label if nam_or_nom == 'NAM' else 'O'  # consider NOM as O

                if index == 0 and current_word:
                    raw_words.append(current_word)
                    current_word = ''

                char_index_list.append(index)
                current_word += char
                current_label.append(label_dict.get(label, 0))
                continue

            raw_words.append(current_word)
            current_word = ''

            multiplied_words = [phrase for phrase in raw_words for _ in range(len(phrase))]

            word_list = []

            raw_chars = [char for phrase in raw_words for char in phrase]  # list化

            for raw_char in raw_chars:
                this_word = []
                for single_char in raw_char:
                    char_index = phrase_dict.get(single_char, 0)
                    this_word.append(char_index)

            for raw_word in multiplied_words:
                try:
                    word_index = phrase_dict[raw_word]
                    word_list.append(word_index)
                except KeyError:
                    word_list.append(0)

            try:
                chars = [character_dict[char] for char in raw_chars]
            except KeyError:
                current_label = []
                raw_words = []
                char_index_list = []
                continue

            radical_raw_list = [char2radical.get(char, 0) for char in raw_chars]

            # 对应data_preprocess/out里的pickle文件
            result.append([
                raw_words,
                raw_chars,
                chars,
                word_list,
                [],
                [],
                radical_raw_list,
                [],
                current_label,
                [],
                [],
                [],
                char_index_list,
                [],
            ])
            current_label = []
            raw_words = []
            char_index_list = []

    if not os.path.exists('process_character/out'):
        os.mkdir('process_character/out')
    with open('process_character/out/' + outname + '.pkl', 'wb') as f:
        pickle.dump(result, f)


def run(entity_type=EntityType.all):
    if os.path.exists('out/train.pkl') and os.path.exists('out/test.pkl') and os.path.exists(
            'out/dev.pkl'):
        print('load existing train/test/dev data...')
        return

    train_file_name = 'process_character/data_preprocess/weiboNER_2nd_conll.train'
    test_file_name = 'process_character/data_preprocess/weiboNER_2nd_conll.test'
    dev_file_name = 'process_character/data_preprocess/weiboNER_2nd_conll.dev'
    file_names = [train_file_name, test_file_name, dev_file_name]

    gen_pure_data()

    for fname in file_names:
        # process_url(fname)
        # remove_english(fname)
        replace_rare_punctuation(fname)

    for fname in file_names:
        suffix = fname.split('.')[-1]
        get_jiebaed_data(fname, suffix, entity_type=entity_type)
