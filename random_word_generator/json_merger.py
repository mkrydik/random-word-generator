import glob
import json
import os
import re
from itertools import groupby
from typing import Dict, List


class JsonMerger:
    """事前に取得した JSON ファイルをマージするクラス"""

    def __init__(self) -> None:
        """この Python ファイルパスを基準に JSON ファイルの取得元ディレクトリを特定し出力用ディレクトリを作っておく"""

        self.raw_json_directory_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./raw_json"))
        self.merged_json_directory_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./merged_json"))
        os.makedirs(self.merged_json_directory_path, exist_ok=True)

    def merge_all(self) -> None:
        """事前に取得した JSON ファイルをマージして出力する"""

        print("Merge All : Start")
        raw_json_files = self.__get_raw_json_files()
        for group_name, file_paths in raw_json_files.items():
            print(f"[{group_name}] ({len(file_paths)}) : Start")
            json_merger.__merge_json_files(group_name, file_paths)
            print(f"[{group_name}] ({len(file_paths)}) : Finished")
        print("Merge All : Finished")

    def __get_raw_json_files(self) -> Dict[str, List[str]]:
        """事前に取得した JSON ファイル名をリストアップしグループ化する

        Return:
            Dict[str, List[str]]: キーが品詞を示すグループ名、値が当該品詞のファイルパスの配列
        """

        # JSON ファイルのフルパスを取得する
        raw_json_file_paths = glob.glob(os.path.normpath(os.path.join(self.raw_json_directory_path, "./*.json")))
        # 品詞別にグループ化する
        grouping_file_paths = list(
            map(
                lambda file_path: dict(
                    group_name=re.sub("_[0-9]{2}$", "", os.path.splitext(os.path.basename(file_path))[0]),  # ファイル名の連番・拡張子部分を除いた文字列
                    file_path=file_path,
                ),
                raw_json_file_paths,
            )
        )
        grouping_file_paths.sort(key=lambda file_path: file_path["group_name"])  # Group By するために事前に Sort する
        file_path_group = groupby(grouping_file_paths, key=lambda file_path: file_path["group_name"])

        # グループを辞書に変換する
        raw_json_files = dict()
        for key, group in file_path_group:
            file_paths = list(map(lambda group_item: group_item["file_path"], list(group)))
            file_paths.sort()  # ファイル名順にソートし直す
            raw_json_files[key] = file_paths
        return raw_json_files

    def __merge_json_files(self, group_name: str, raw_json_file_paths: List[str]) -> None:
        """JSON ファイルを読み込みマージし、不要な項目を削除して出力する

        Args:
            group_name (str): 品詞を示すグループ名・出力ファイル名になる
            raw_json_file_paths (List[str]): 当該グループの取得元ファイルパスの配列
        """

        # 各 JSON ファイルの配列をマージする
        all_titles = list()
        for raw_json_file_path in raw_json_file_paths:
            with open(raw_json_file_path, "r") as raw_json_file:
                all_titles.extend(json.load(raw_json_file))

        # 不要な項目を削除する
        titles = list(filter(lambda title: ":" not in title, all_titles))

        merged_json_file_path = os.path.normpath(os.path.join(self.merged_json_directory_path, f"./{group_name}.json"))
        with open(merged_json_file_path, mode="wt", encoding="utf-8") as merged_json_file:
            json.dump(titles, merged_json_file, ensure_ascii=False)
            merged_json_file.write("\n")


if __name__ == "__main__":
    json_merger = JsonMerger()
    json_merger.merge_all()
