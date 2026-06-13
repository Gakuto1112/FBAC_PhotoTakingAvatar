import json
from pathlib import Path
from typing import Any, TypeAlias


BBModelData: TypeAlias = dict[str, Any]
"""
BBモデルのデータであると示す型エイリアス
"""


def read_bbmodel(bbmodel_path: Path) -> BBModelData:
    """
    指定されたパスのBBModelファイルを読み込み、そのデータを辞書型で返す。

    Args:
        bbmodel_path (Path): 読み込むBBModelファイルのパス

    Returns:
        BBModelData: 読み込んだBBModelファイルのデータを格納した辞書

    Raises:
        FileNotFoundError: 指定されたパスにBBModelファイルが存在しない場合
        IsADirectoryError: 指定されたパスがディレクトリである場合
        PermissionError: 指定されたパスのファイルに対する読み取り権限がない場合
        IOError: その他の入出力エラーが発生した場合
        json.JSONDecodeError: BBModelファイルの内容が有効なJSON形式でない場合
    """

    with bbmodel_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def remove_texture_absolute_paths(bbmodel_data: BBModelData) -> BBModelData:
    """
    BBModelデータ内のテクスチャの絶対パスを削除し、変更後のBBModelデータを返す。
    BBModelデータ内のテクスチャには相対パスもあるため、絶対パスは不要である。

    Args:
        bbmodel_data (BBModelData): テクスチャの絶対パスを削除するBBModelデータ

    Returns:
        BBModelData: テクスチャの絶対パスが削除されたBBModelデータ
    """

    if "textures" in bbmodel_data:
        for texture in bbmodel_data["textures"]:
            if "path" in texture:
                del texture["path"]

    return bbmodel_data

if __name__ == "__main__":
    main()
