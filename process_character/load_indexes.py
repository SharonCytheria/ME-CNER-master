import os
import pickle

import jieba

from process_character.constants import Dataset

comps = []
# radicals = []
characters = []
phrases = []
syllables = []

# ============Deleted ====================
# def load_radical_indexes():
#     if not os.path.exists('/Users/sharoncytheria/Downloads/ME-CNER-master/
#     process_character/data_preprocess/radical_indexes.txt'):
#         with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/radical.txt',
#         'r', encoding='utf-8') as f:
#             for line in f:
#                 radicals.extend(line.split())
#
#         with open('/Users/sharoncytheria/Downloads/ME-CNER-master/
#         process_character/data_preprocess/radical_indexes.txt', 'w',
#                   encoding='utf-8') as f:
#             i = 1
#             for radical in radicals:
#                 f.write('%s %s\n' % (i, radical))
#                 i = i + 1
#
#     radical_dict = {}
#     with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/
#     data_preprocess/radical_indexes.txt', 'r', encoding='utf-8') as f:
#         for line in f:
#             index_radical_pair = line.split()
#             radical_dict[int(index_radical_pair[0])] = index_radical_pair[1]
#             radical_dict[index_radical_pair[1]] = int(index_radical_pair[0])
#
#     return radical_dict


def load_character_indexes():
    char_index_dict = {}
    char_index_count = 1
    #  weibo_raw_data即weiboNER_2nd_conll三个数据集的集合,即为"字0 1"的结构
    with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/weibo_raw_data.txt',
              'r', encoding='utf-8') as f:
        for line in f:
            # 如果当前行为空，跳下一行；即一句话结束
            if not line.strip():
                continue

            char, _ = line.split()
            char = char[0]  # 仅提取出char
            # 如果char不在字典中，把char添加到dict中。
            if char not in char_index_dict:
                char_index_dict[char] = char_index_count
                char_index_dict[char_index_count] = char
                char_index_count += 1
            # characters? 句子？保存一句一句话，
            characters.append(line[0])
    return char_index_dict


def load_phrase_indexes():
    #  生成phrase_indexes.txt
    if not os.path.exists('/Users/sharoncytheria/Downloads/ME-CNER-master/'
                          'process_character/data_preprocess/phrase_indexes.txt'):

        with open('process_character/data_preprocess/weibo_raw_data.txt', 'r', encoding='utf-8') as f:
            phrase_list = []
            sentence = []
            for line in f:
                # 句子结束，换行
                if not line.strip():
                    #  表示当前行为空，一句话结束，对之前存储的句子进行词组保存
                    words = list(jieba.cut(''.join(sentence)))
                    phrase_list.extend(words)
                    sentence = []
                    continue
                # 处理句子，将一个句子中的每一个char连接成一个完整的句子 ？
                # 连接完后通过结巴分词，将句子进行分词，存储到词组list中。
                # sentence仅用于暂存句子。
                # 最终想要得到的是phrase_list
                char, _ = line.split()
                char = char[0]
                sentence.append(char)

        # 将原列表去重，并按从小到大排序
        # 因为在我们的数据集中，phrase_list中可能存在相同的从不同句子中分词出来的词组。
        # 在这个地方，我们对相同的词组进行去重，仅保留一个，并按照一定规则从小到大排序。
        phrase_set = list(set(phrase_list))
        phrase_set.sort(key=phrase_list.index)
        with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/phrase_indexes.txt',
                  'w', encoding='utf-8') as f:
            i = 1
            for phrase in phrase_set:
                if not phrase:
                    continue
                f.write('%s %s\n' % (i, phrase))
                i = i + 1

    phrase_dict = {}
    with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/phrase_indexes.txt',
              'r', encoding='utf-8') as f:
        for line in f:
            if not line.split():
                continue

            index_phrase_pair = line.split()
            phrase_dict[int(index_phrase_pair[0])] = index_phrase_pair[1]
            phrase_dict[index_phrase_pair[1]] = int(index_phrase_pair[0])

    return phrase_dict


def load_msra_character_indexes():
    char_index_dict = {}
    char_index_count = 1
    with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/msra_raw_data.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            char, _ = line.split()
            char = char[0]
            if char not in char_index_dict:
                char_index_dict[char] = char_index_count
                char_index_dict[char_index_count] = char
                char_index_count += 1
            characters.append(line[0])
    return char_index_dict


def load_msra_phrase_indexes():
    if not os.path.exists('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/msra_phrase_indexes.txt'):

        with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/msra_raw_data.txt', 'r', encoding='utf-8') \
                as f:
            phrase_list = []
            sentence = []
            for line in f:
                if not line.strip():
                    words = list(jieba.cut(''.join(sentence)))
                    phrase_list.extend(words)
                    sentence = []
                    continue

                char, _ = line.split()
                char = char[0]
                sentence.append(char)

        phrase_set = list(set(phrase_list))
        phrase_set.sort(key=phrase_list.index)
        with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/msra_phrase_indexes.txt', 'w',
                  encoding='utf-8') as f:
            i = 1
            for phrase in phrase_set:
                if not phrase:
                    continue
                f.write('%s %s\n' % (i, phrase))
                i = i + 1

    phrase_dict = {}
    with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/msra_phrase_indexes.txt', 'r', encoding='utf-8') \
            as f:
        for line in f:
            if not line.split():
                continue

            index_phrase_pair = line.split()
            phrase_dict[int(index_phrase_pair[0])] = index_phrase_pair[1]
            phrase_dict[index_phrase_pair[1]] = int(index_phrase_pair[0])

    return phrase_dict


def load_label_indexes(dataset_type):
    label_dict = {}
    with open('/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/%slabel_indexes.txt' %
              ('msra_' if dataset_type == Dataset.MSRA else ''),
              'r', encoding='utf-8') as f:
        for line in f:
            index_label_pair = line.split()
            label_dict[int(index_label_pair[0])] = index_label_pair[1]
            label_dict[index_label_pair[1]] = int(index_label_pair[0])

    return label_dict
