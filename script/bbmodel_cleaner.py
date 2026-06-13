import json
from pathlib import Path

def read_bbmodel(bbmodel_path: Path) -> dict:
    """
    指定されたパスのBBModelファイルを読み込み、そのデータを辞書型で返す。

    Args:
        bbmodel_path (Path): 読み込むBBModelファイルのパス

    Returns:
        dict: 読み込んだBBModelファイルのデータを格納した辞書

    Raises:
        FileNotFoundError: 指定されたパスにBBModelファイルが存在しない場合
        IsADirectoryError: 指定されたパスがディレクトリである場合
        PermissionError: 指定されたパスのファイルに対する読み取り権限がない場合
        IOError: その他の入出力エラーが発生した場合
        json.JSONDecodeError: BBModelファイルの内容が有効なJSON形式でない場合
    """

    with bbmodel_path.open("r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    main()
