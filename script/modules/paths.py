from dataclasses import dataclass
from pathlib import Path


@dataclass
class AvatarPaths:
	root: Path = Path(__file__).parent.resolve()
	"""
	レポジトリのルートディレクトリ
	"""

	_input_dir: Path = root / "src" / "models"
	"""
	ソースファイルが格納されるディレクトリ
	"""

	_output_dir: Path = root / "src" / "models"
	"""
	ビルド済みアバターの出力先ディレクトリ
	"""

	@property
	def input_dir(self) -> Path:
		"""
		入力ディレクトリのパス
		"""

		return self._input_dir

	@input_dir.setter
	def input_dir(self, path: Path) -> None:
		"""
		input_dirのセッター関数

		Args:
			path (Path): input_dirのパス
		"""

		self._input_dir = path

	@property
	def output_dir(self) -> Path:
		"""
		出力ディレクトリのパス
		"""

		return self._output_dir

	@output_dir.setter
	def output_dir(self, path: Path) -> None:
		"""
		output_dirのセッター関数

		Args:
			path (Path): output_dirのパス
		"""

		self._output_dir = path

	@staticmethod
	def prepare_output_directory() -> None:
		"""
		出力ディレクトリが存在しない場合は作成する。

		Raises:
			PermissionError: 出力ディレクトリを作成するための権限がない場合
			IOError: その他の入出力エラーが発生した場合
		"""

		if not paths.output_dir.exists():
			paths.output_dir.mkdir(parents=True, exist_ok=True)

paths = AvatarPaths()
