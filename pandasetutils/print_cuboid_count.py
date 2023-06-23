import argparse
import copy
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas
from pandaset import DataSet

from pandasetutils.common.utils import set_logger

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CuboidCounts:
    sequence_id: str
    frame_no: int
    counts: dict[str, int]
    """keyがlabel, valueがオブジェクト数であるdict"""


class DataSetAccessor:
    def __init__(self, dataset: DataSet) -> None:
        self.dataset = dataset

    def get_cuboid_counts_list(self, sequence_id: str) -> list[CuboidCounts]:
        """

        keyは
        """
        sequence = self.dataset[sequence_id]
        sequence.load_cuboids()

        result: list[CuboidCounts] = []
        try:
            for frame_no, df in enumerate(sequence.cuboids.data):
                counter = Counter(df["label"])
                result.append(CuboidCounts(sequence_id=sequence_id, frame_no=frame_no, counts=counter))
        finally:
            self.dataset.unload(sequence_id)

        return result


def create_cuboid_counts_dataframe(input_dir: Path, sequence_id_list: None | list[str] = None) -> pandas.DataFrame:
    """
    labelごとのcuboidのオブジェクト数が格納された`pandas.DataFrame`を生成します。

    Args:
        pandasetのディレクトリ
        sequence_id_list: 取得対象のsequence_idのlist。Noneならば全てのsequence_idが取得対象になります。
    Returns:
        index: sequence_id, frame_no
        columns: cuboidのlabel
    """
    dataset = DataSet(str(input_dir))
    _sequence_id_list = sequence_id_list if sequence_id_list is not None else dataset.sequences()

    dataset_accessor = DataSetAccessor(dataset)

    data: list[dict[str, Any]] = []
    for sequence_id in _sequence_id_list:
        logger.debug(f"{sequence_id=} :: cuboidのlabelごとのオブジェクト数を取得します。")

        try:
            cuboid_counts_list = dataset_accessor.get_cuboid_counts_list(sequence_id)
            for cuboid_counts in cuboid_counts_list:
                tmp: dict[str, Any] = copy.deepcopy(cuboid_counts.counts)
                tmp["frame_no"] = cuboid_counts.frame_no
                tmp["sequence_id"] = cuboid_counts.sequence_id
                data.append(tmp)
        except Exception:
            logger.warning(f"{sequence_id=} :: labelごとのオブジェクト数の取得に失敗しました。", exc_info=True)
            continue

    df = pandas.DataFrame(data)
    df = df.fillna(0)
    df = df.set_index(["sequence_id", "frame_no"])

    # columnを辞書順に並び替える
    df = df[sorted(df.columns)]
    return df


def main() -> None:
    args = parse_args()
    set_logger()

    df = create_cuboid_counts_dataframe(args.input_dir, args.sequence_id)
    output_file = args.output_csv
    output_file.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(str(output_file))


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description="cuboidのlabelごとのオブジェクト数をCSV形式で出力します。",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_dir", type=Path, required=True, help="pandasetのディレクトリ")
    parser.add_argument("output_csv", type=Path, required=True, help="CSVファイルの出力先")
    parser.add_argument(
        "--sequence_id", type=str, nargs="+", required=False, help="集計対象のsequence id。未指定ならばすべてのsequence idが対象です。"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
    main()
