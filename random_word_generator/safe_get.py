from functools import reduce
from typing import Any, Dict, Mapping, Union


def safe_get(dictionary: Union[Dict, Mapping[Any, Any]], *keys: str) -> Union[Any, None]:
    """ネストされた辞書からでも例外を発生させず安全にデータを取得する
    
    Args:
        dictionary (Union[Dict, Mapping[Any, Any]]): 辞書
        *keys (str): キー名・ネストする場合は複数の引数を指定する
    
    Return:
        Union[Any, None]: 値が取得できればその値、取得できなければ None を返す
    """
    
    return reduce(lambda value, key: value.get(key) if value else None, keys, dictionary)  # type: ignore
