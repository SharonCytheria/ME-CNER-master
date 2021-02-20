import os
import jieba


def process_drink_data(
        input_file='/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/data_preprocess/drinks/drinks.',
        output_file='/Users/sharoncytheria/Downloads/ME-CNER-master/process_character/'
                    'data_preprocess/drinks/jiebaed_drinks.',
        suffixes=('train', 'test', 'dev')
):
    #  转weiboNER_2nd_conll为相对应的weibo_pure_data
    for suffix in suffixes:
        with open(input_file + suffix, 'r', encoding='utf-8') as f:
            result = []
            for line in f:
                parts = line.split()
                sentence = str(parts[1:])
                words = jieba.cut(sentence[2:-2], cut_all=False)
                # print("Full Mode: " + "/ ".join(words))
                result.append("/".join(words) + "\n")

        with open(output_file + suffix, 'w', encoding='utf-8') as f:
            # for sentence in result:
            #     f.write('%s %s\n' % (i, sentence))
            #     i += 1
            f.writelines(result)


process_drink_data()
