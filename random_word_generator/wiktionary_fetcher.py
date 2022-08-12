import json
import os
from typing import List, Optional, TypedDict

import requests

from random_word_generator.safe_get import safe_get


class FetchResult(TypedDict):
    """Wiktionary API のレスポンスデータを控えるオブジェクト"""

    titles: List[str]
    """子カテゴリ名の配列"""
    cmcontinue: Optional[str]
    """当該記事に続きのコンテンツがある場合は続きのコンテンツを取得するための文字列が設定される"""


class WiktionaryFetcher:
    """Wiktionary API をコールして単語一覧を取得・JSON の配列としてファイルに出力するクラス"""

    def __init__(self) -> None:
        """この Python ファイルパスを基準に JSON ファイルの出力用ディレクトリを作っておく"""

        self.raw_json_directory_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./raw_json"))
        os.makedirs(self.raw_json_directory_path, exist_ok=True)

    def fetch_all(self, cmtitle: str, file_name: str) -> None:
        """指定の記事の全ての子カテゴリ情報を取得・ファイルに出力する

        Note:
            子カテゴリ (`categorymembers`) 情報は1度に最大500件までしか取得できず、続きのコンテンツがある場合は API が `cmcontinue` をレスポンスする
            そこで API を複数回コールして全ての情報を取得する

        Args:
            cmtitle (str): Wiktionary の記事タイトル
            file_name (str): 出力するファイル名
        """

        print(f"Fetch All : Start [{cmtitle}] -> [{file_name}]")
        num = 0
        cmcontinue = None
        while True:  # `do while`
            print(f"  [{num}] Start [{cmcontinue}]")
            fetch_result = self.__fetch(cmtitle, cmcontinue)
            file_path = self.__make_file_path(file_name, num)
            self.__write_json(file_path, fetch_result["titles"])
            cmcontinue = safe_get(fetch_result, "cmcontinue")
            if cmcontinue is None:
                print(f"  [{num}] Break")
                break
            else:
                print(f"  [{num}] Continue [{cmcontinue}]")
                num += 1
        print(f"Fetch All : Finished [{cmtitle}] -> [{file_name}]")

    def __fetch(self, cmtitle: str, cmcontinue: Optional[str] = None) -> FetchResult:
        """Wiktionary API をコールして記事を取得する

        Args:
            cmtitle (str): Wiktionary の記事タイトル
            cmcontinue (Optional[str], optional): 値を指定した場合、その続きのコンテンツ部分を取得する

        Return:
            FetchResult: 取得結果オブジェクト
        """

        params = {"format": "json", "action": "query", "cmtitle": cmtitle, "list": "categorymembers", "cmlimit": "500"}  # 最大500まで
        if cmcontinue is not None:
            params["cmcontinue"] = cmcontinue

        response = requests.get("https://ja.wiktionary.org/w/api.php", params)
        response_json = response.json()

        category_members = safe_get(response_json, "query", "categorymembers")
        titles = list(map(lambda category_member: safe_get(category_member, "title"), category_members))  # type: ignore

        fetch_result = FetchResult(titles=titles, cmcontinue=safe_get(response_json, "continue", "cmcontinue"))  # type: ignore
        return fetch_result

    def __make_file_path(self, file_name: str, num: int) -> str:
        """出力する JSON ファイルのフルパスを生成する

        Args:
            file_name (str): ファイル名
            num (int): 連番・2桁のゼロパディングに変換して使用する

        Return:
            str: 出力する JSON ファイルのフルパス
        """

        zero_pad_num = str(num).zfill(2)
        file_path = os.path.join(self.raw_json_directory_path, f"./{file_name}_{zero_pad_num}.json")
        return os.path.normpath(file_path)

    def __write_json(self, file_path: str, titles: List[str]) -> None:
        """JSON ファイルを出力する

        Args:
            file_path (str): 出力先・フルパス
            titles (List[str]): 子カテゴリ名の配列
        """

        with open(file_path, mode="wt", encoding="utf-8") as file:
            json.dump(titles, file, ensure_ascii=False, indent=2)
            file.write("\n")


if __name__ == "__main__":
    wiktionary_fetcher = WiktionaryFetcher()
    wiktionary_fetcher.fetch_all("カテゴリ:日本語_名詞", "nouns")  # 'cmpageid': '7813'
    wiktionary_fetcher.fetch_all("カテゴリ:日本語_形容詞", "adjectives")  # 'cmpageid': '8497'
    wiktionary_fetcher.fetch_all("カテゴリ:日本語_形容動詞", "adjectival_nouns")  # 'cmpageid': '8458'
    wiktionary_fetcher.fetch_all("カテゴリ:日本語_動詞", "verbs")  # 'cmpageid': '8459'
    wiktionary_fetcher.fetch_all("カテゴリ:日本語_副詞", "adverbs")  # 'cmpageid': '8668'
