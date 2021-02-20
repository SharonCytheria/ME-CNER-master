import os


def concat_weibo():
    """
    CONCAT三个数据集
    :return:
    """
    if not os.path.exists('process_character/data_preprocess/weibo_raw_data.txt'):
        lines = []
        for file_suffix in ['train', 'test', 'dev']:
            with open('process_character/data_preprocess/weiboNER_2nd_conll.%s' % file_suffix, 'r',
                      encoding='utf-8') as f:
                for line in f:
                    lines.append(line)

        with open('process_character/data_preprocess/weibo_raw_data.txt', 'w', encoding='utf-8') as f:
            f.writelines(lines)
    print("Done with Weibo")


def concat_drinks():
    if not os.path.exists('/Users/sharoncytheria/Downloads/ME-CNER-master/'
                          'process_character/data_preprocess/drinks/drinks_raw_data.txt'):
        lines = []
        for file_suffix in ['train', 'test', 'dev']:
            with open('/Users/sharoncytheria/Downloads/ME-CNER-master/'
                      'process_character/data_preprocess/drinks/drinks.%s' % file_suffix, 'r', encoding='utf8') as f:
                for line in f:
                    lines.append(line)
        # print(lines)
        with open('process_character/data_preprocess/drinks/drink_raw_data.txt', 'w', encoding='utf-8') as f:
            f.writelines(lines)
    print("Done with Drinks")


def concat_msra():
    """
    CONCAT三个数据集
    :return:
    """
    if not os.path.exists('process_character/data_preprocess/msra_raw_data.txt'):
        lines = []
        for file_suffix in ['train', 'test', 'dev']:
            with open('process_character/data_preprocess/msra.%s' % file_suffix, 'r',
                      encoding='utf-8') as f:
                for line in f:
                    lines.append(line)

        with open('process_character/data_preprocess/msra_raw_data.txt', 'w', encoding='utf-8') \
                as f:
            f.writelines(lines)
    print("Done with MSRA")


if __name__ == '__main__':
    # concat_weibo()
    concat_drinks()
    # concat_msra()
