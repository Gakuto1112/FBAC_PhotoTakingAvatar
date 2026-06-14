import argparse
import errno
import json
from pathlib import Path
from typing import Any, TypeAlias
import re

from modules.logger import Logger
from modules.paths import paths


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

def write_bbmodel_data(bbmodel_path: Path, bbmodel_data: BBModelData) -> None:
    """
    指定されたパスのBBModelファイルに、指定されたデータを書き込む。
    BBModelのフォーマットに合うようにJSON整形も行う。

    Args:
        bbmodel_path (Path): 書き込むBBModelファイルのパス
        bbmodel_data (BBModelData): 書き込むBBModelデータを格納した辞書

    Raises:
        IsADirectoryError: 指定されたパスがディレクトリである場合
        PermissionError: 指定されたパスのファイルに対する書き込み権限がない場合
        IOError: その他の入出力エラーが発生した場合
    """

    with bbmodel_path.open("w", encoding="utf-8") as f:
        f.write(format_bbmodel_to_json(bbmodel_data))

def format_bbmodel_to_json(bbmodel_data: BBModelData) -> str:
    """
    BBModelデータをJSON形式の文字列に変換する。
    BBModelファイルのJSON形式に合うように整形も行う。

    Args:
        bbmodel_data (BBModelData): JSON形式の文字列に変換するBBModelデータを格納した辞書

    Returns:
        str: BBModelデータをJSON形式に変換した文字列
    """

    def replacer(match: re.Match) -> str:
        """
        BBModelのJSON配列/オブジェクトのリプレイサー関数。
        配列やオブジェクトの文字数が118文字以下の場合は、改行とスペースを削除して1行にまとめる。
        118文字を超える場合は、元の文字列をそのまま返す。

        Args:
            match (re.Match): 正規表現のマッチオブジェクト

        Returns:
            str: 整形された文字列
        """

        substring = match.group(0)
        substring = re.sub(r"\n\s*", "", substring)
        if len(substring) <= 118:
            substring = substring.replace(",", ", ")
        return substring

    json_string = json.dumps(bbmodel_data, ensure_ascii=False, indent="\t")
    json_string = re.sub(r"\[[^\[\]{}]+\]", replacer, json_string)

    return json_string

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

def cleanup_bbmodel(bbmodel_data: BBModelData) -> BBModelData:
    """
    BBモデルファイルの構造から無駄なデータを省き、クリーンアップする。

    Args:
        bbmodel_data (BBModelData): クリーンアップするBBモデルデータ

    Returns:
        BBModelData: クリーンアップされたBBモデルデータ
    """

    cleaned_data = remove_texture_absolute_paths(bbmodel_data)

    return cleaned_data

def main() -> None:
    """
    エントリー関数
    """

    # 引数の設定
    parser = argparse.ArgumentParser(description="Cleans up a BBModel file by removing unnecessary data.")

    parser.add_argument("-i", "--input-dir", type=str, default=paths.input_dir, help="Overrides default input directory path. Default: ../src/models/")
    parser.add_argument("-o", "--output-dir", type=str, default=paths.output_dir, help="Overrides default output directory path. Default: ../src/models/")
    parser.add_argument("-c", "--colored", action="store_true", help="Enables colored output in the terminal.")
    parser.add_argument("-d", "--debug-output", action="store_true", help="Enables debug outputs.")

    args = parser.parse_args()

    # 引数の処理
    paths.input_dir = Path(args.input_dir)
    paths.output_dir = Path(args.output_dir)
    if args.colored:
        Logger.is_colored = True
    if args.debug_output:
        Logger.should_print_debug_log = True
    Logger.print_info("Model cleaner script for BlockBench models (.bbmodel)")
    Logger.print_spacer(1)

    # デバッグ出力
    if Logger.should_print_debug_log:
        Logger.print_debug(f"Debug output enabled.")
        Logger.print_spacer(1)

        Logger.print_debug("Test output for debug level log.")
        Logger.print_info("Test output for info level log.")
        Logger.print_warning("Test output for warning level log.")
        Logger.print_error("Test output for error level log.")
        Logger.print_spacer(1)

    Logger.print_debug(f"Input directory: {paths.input_dir}")
    Logger.print_debug(f"Output directory: {paths.output_dir}")
    Logger.print_debug(f"Colored output: {'enabled' if Logger.is_colored else 'disabled'}")
    Logger.print_spacer(1)

    # 出力ディレクトリの準備
    try:
        if not paths.output_dir.exists():
            Logger.print_info("Output directory does not exist. Attempting to create it...")
            paths.prepare_output_directory()
            Logger.print_spacer(1)
    except ValueError:
        Logger.print_error(f"Invalid path for output directory: {paths.output_dir}")
        exit(errno.EINVAL)
    except PermissionError:
        Logger.print_error("No permission to create output directory.")
        exit(errno.EACCES)
    except IOError as error:
        Logger.print_error(f"An unexpected error occurred while preparing the output directory: {error}")
        exit(errno.EIO)

    # BBモデルファイルのクリーンアップ
    for bbmodel_path in paths.input_dir.rglob("*.bbmodel"):
        Logger.print_info(f"Cleaning up bbmodel file: {bbmodel_path.name}...")
        try:
            bbmodel_data = read_bbmodel(bbmodel_path)
            cleaned_data = cleanup_bbmodel(bbmodel_data)
            write_bbmodel_data(paths.output_dir / bbmodel_path.name, cleaned_data)
        except FileNotFoundError:
            Logger.print_error(f"BBModel file not found: {bbmodel_path}")
        except IsADirectoryError:
            Logger.print_error(f"Expected a file but found a directory: {bbmodel_path}")
        except PermissionError:
            Logger.print_error(f"No permission to read or write the file: {bbmodel_path}")
        except IOError as error:
            Logger.print_error(f"An unexpected error occurred while processing the file {bbmodel_path}: {error}")
        except json.JSONDecodeError:
            Logger.print_error(f"Invalid JSON format in BBModel file: {bbmodel_path}")
    Logger.print_info("Completed cleaning up BBModel files.")

if __name__ == "__main__":
    main()
