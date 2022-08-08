import glob
import json
import os
import random
import sys


def main() -> None:
    """ランダムな言葉を生成する"""
    
    default_num =  1  # 生成する言葉のデフォルト数
    max_num     = 50  # 生成する言葉の最大数
    
    min_words   =  1  # 1つの言葉に含める最小の単語数
    max_words   =  5  # 1つの言葉に含める最大の単語数
    
    # 生成する言葉の数・デフォルトは1件
    number_to_generate = default_num
    
    # コマンドライン引数で生成する言葉の数の指定があれば受け付ける
    args = sys.argv
    if len(args) == 2:
        raw_num = args[1]
        num = int(raw_num) if raw_num.isdigit() else default_num  # コマンドライン引数が数値でなければデフォルト値のままとする
        number_to_generate = max_num if num > max_num else default_num if num < default_num else num  # 大き過ぎる値・ゼロや負数は調整する
    
    # 品詞別の単語一覧 JSON ファイルのパスを取得する
    merged_json_directory_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), './merged_json'))
    json_file_paths = glob.glob(os.path.normpath(os.path.join(merged_json_directory_path, './*.json')))
    
    # 品詞別に単語一覧を取得し保持する
    parts_of_speech = dict()
    for json_file_path in json_file_paths:
        with open(json_file_path, 'r') as json_file:
            part_of_speech = os.path.splitext(os.path.basename(json_file_path))[0]
            parts_of_speech[part_of_speech] = json.load(json_file)
    # [print(f'[{pos_name}] ({len(words)})') for pos_name, words in list(parts_of_speech.items())]  # デバッグ用・品詞別単語数
    
    # ランダムな単語を生成する
    for _ in range(number_to_generate):
        number_of_words = random.randint(min_words, max_words)  # 抽出する単語数
        random_words = ''
        for _ in range(number_of_words):
            # 品詞を一つ決める
            pos_name = random.choice(list(parts_of_speech.keys()))
            # 当該品詞から一つ単語を取得する
            random_word = random.choice(parts_of_speech[pos_name])
            random_words += random_word
        # 出力する
        print(random_words)


if __name__ == '__main__':
    main()
