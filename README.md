# Random Word Generator

ランダムな言葉を生成する CLI ツールです。


## 使い方

最初に [Poetry](https://python-poetry.org/) で仮想環境を構築し依存パッケージをインストールしてください。

```bash
# Poetry で仮想環境を構築する
$ git clone https://github.com/mkrydik/random-word-generator.git && cd "$(basename "$_" .git)"
$ poetry install
```

なお、このプロジェクトは以下の環境で動作確認しています。

- WSL2 Ubuntu v20.04.4 : Python v3.8.10 : Poetry v1.1.14
- macOS Monterey v12.4 : Python v3.8.9 : Poetry v1.1.14

実行するには次のように `$ python -m random_word_generator` で実行できます。

```bash
# Poetry Shell 内で実行する場合
$ poetry shell
$$ python -m random_word_generator
ちかごろゆるいかよわい悲惨ちなまぐさい
# ↑ このようにランダムな言葉が出力されます

# Poetry Run で直接実行する場合
$ poetry run python -m random_word_generator
思う存分ニュートンはがれる
# ↑ このようにランダムな言葉が出力されます
```

第1引数に整数を入れると、その数だけ一度に複数の言葉を生成します。一度に生成できる言葉は `50` 個までに制限してあります。

```bash
# 5つの言葉を一度に生成します
$ poetry run python -m random_word_generator 5
ほとんどサンライズ
スレンダーば行
悲観的ベイビー
うしろめたい対等
革新的おくば
```


## 単語データの準備手順

生成する単語データは [Wiktionary 日本語版](https://ja.wiktionary.org/) より収集しています。

- [カテゴリ:日本語 名詞](https://ja.wiktionary.org/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E6%97%A5%E6%9C%AC%E8%AA%9E_%E5%90%8D%E8%A9%9E)
- [カテゴリ:日本語 形容詞](https://ja.wiktionary.org/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E6%97%A5%E6%9C%AC%E8%AA%9E_%E5%BD%A2%E5%AE%B9%E8%A9%9E)
- [カテゴリ:日本語 形容動詞](https://ja.wiktionary.org/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E6%97%A5%E6%9C%AC%E8%AA%9E_%E5%BD%A2%E5%AE%B9%E5%8B%95%E8%A9%9E)
- [カテゴリ:日本語 動詞](https://ja.wiktionary.org/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E6%97%A5%E6%9C%AC%E8%AA%9E_%E5%8B%95%E8%A9%9E)
- [カテゴリ:日本語 副詞](https://ja.wiktionary.org/wiki/%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA:%E6%97%A5%E6%9C%AC%E8%AA%9E_%E5%89%AF%E8%A9%9E)

これらのページより子ページの一覧情報を単語データとして利用しています。[MediaWiki API](https://ja.wiktionary.org/w/api.php) を使用して子ページの情報を収集し `./random_word_generator/raw_json/` 配下にファイルを溜め込むのが以下のスクリプトです。

```bash
$ poetry run python ./random_word_generator/wiktionary_fetcher.py
```

`raw_json/` ディレクトリにファイル群が用意できたら、次のスクリプトを実行することで `./random_word_generator/merged_json/` ディレクトリ配下にマージした JSON ファイルを生成します。

```bash
$ poetry run python ./random_word_generator/json_merger.py
```

本スクリプトは、この `merged_json/` ディレクトリ配下にある JSON ファイル群を読み取って言葉を生成しています。各 JSON ファイルはトップレベルが配列、各要素は文字列であることが求められます。

現状、品詞別に JSON ファイルを分割しているものの、品詞は区別せず完全ランダムに単語を結合しています。単語データの精査もしていないので、日本語として自然な言葉とはいえませんが、意外な言葉の組み合わせを眺めてみてください。


## コーディング関連コマンド

```bash
# mypy : Static Type Check
$ poetry run python -m mypy ./

# Flake8 : Style Check
$ poetry run python -m flake8 ./

# Black : Auto Formatter (Preview Only)
$ poetry run python -m black --diff --color ./

# isort : Sort Imports (Preview Only)
$ poetry run python -m isort --diff ./

# pytest : Test Codes
$ poetry run python -m pytest
```
