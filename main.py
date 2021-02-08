# -*- coding: utf-8 -*-
import argparse

from entity_type import EntityType
from process_character.load_embedding_data import run as run_load_embedding_data
from process_character.load_weibo_data import run as run_load_weibo_data
from train_ner.model import run as run_train
from train_status import TrainConf

if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # 创建一个解析器 括号里可以有description ArgumentParser
    # ArgumentParser对象包含将命令行解析成 Python 数据类型所需的全部信息
    # parser = argparse.ArgumentParser(description="It's a description which can be seen in the terminal.")
    # 给ArgumentParser添加程序参数信息是通过函数add_argument()实现的。
    # 通常，这些调用指定 ArgumentParser 如何获取命令行字符串并将其转换为对象。这些信息在 parse_args() 调用时被存储和使用。
    # 默认参数，dataset=weibo, with_radical, conv_gru, bigru_crf, all.
    # parser.add_argument('--dataset', default=TrainConf.weibo)  # 默认是TrainConf中的weibo dataset
    parser.add_argument('--dataset', default=TrainConf.drink)  # 我们的drink dataset
    parser.add_argument('--with_radical', default=TrainConf.with_radical)
    parser.add_argument('--network', default=TrainConf.conv_gru)
    parser.add_argument('--tagger', default=TrainConf.bigru_crf)
    parser.add_argument('--entity_type', default=EntityType.all)
    args = parser.parse_args()  # 存储并使用
    entity_type = args.entity_type

    run_load_weibo_data(entity_type=entity_type)
    run_load_embedding_data()
    run_train(conf={
        'dataset': args.dataset,
        'with_radical': int(args.with_radical),
        'network': args.network,
        'tagger': args.tagger,
    })


