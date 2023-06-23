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

SEMSEG_CLASSES = {
    "1": "Smoke",
    "2": "Exhaust",
    "3": "Spray or rain",
    "4": "Reflection",
    "5": "Vegetation",
    "6": "Ground",
    "7": "Road",
    "8": "Lane Line Marking",
    "9": "Stop Line Marking",
    "10": "Other Road Marking",
    "11": "Sidewalk",
    "12": "Driveway",
    "13": "Car",
    "14": "Pickup Truck",
    "15": "Medium-sized Truck",
    "16": "Semi-truck",
    "17": "Towed Object",
    "18": "Motorcycle",
    "19": "Other Vehicle - Construction Vehicle",
    "20": "Other Vehicle - Uncommon",
    "21": "Other Vehicle - Pedicab",
    "22": "Emergency Vehicle",
    "23": "Bus",
    "24": "Personal Mobility Device",
    "25": "Motorized Scooter",
    "26": "Bicycle",
    "27": "Train",
    "28": "Trolley",
    "29": "Tram / Subway",
    "30": "Pedestrian",
    "31": "Pedestrian with Object",
    "32": "Animals - Bird",
    "33": "Animals - Other",
    "34": "Pylons",
    "35": "Road Barriers",
    "36": "Signs",
    "37": "Cones",
    "38": "Construction Signs",
    "39": "Temporary Construction Barriers",
    "40": "Rolling Containers",
    "41": "Building",
    "42": "Other Static Object",
}
"""
semsegのidとnameのdict
`sequence.semseg.classes`から取得した情報
"""


@dataclass(frozen=True)
class SemsegCounts:
    sequence_id: str
    frame_no: int
    point_counts: dict[str, int]
    """keyがlabel, valueが点の個数であるdict"""


class DataSetAccessor:
    def __init__(self, dataset: DataSet) -> None:
        self.dataset = dataset

    def get_semseg_counts_list(self, sequence_id: str) -> list[SemsegCounts]:
        """

        keyは
        """
        sequence = self.dataset[sequence_id]
        sequence.load_semseg()

        result: list[SemsegCounts] = []
        try:
            if sequence.semseg is None:
                logger.warning(f"{sequence_id=} :: semsegデータが存在しません。")
                return []

            for frame_no, df in enumerate(sequence.semseg.data):
                counter = Counter(df["class"])
                result.append(SemsegCounts(sequence_id=sequence_id, frame_no=frame_no, point_counts=counter))
        finally:
            self.dataset.unload(sequence_id)

        return result


def create_semseg_point_counts_dataframe(input_dir: Path, sequence_id_list: None | list[str] = None) -> pandas.DataFrame:
    """
    labelごとのsemsegの点の個数が格納された`pandas.DataFrame`を生成します。

    Args:
        pandasetのディレクトリ
        sequence_id_list: 取得対象のsequence_idのlist。Noneならば全てのsequence_idが取得対象になります。

    Returns:
        index: sequence_id, frame_no
        columns: cuboidのlabel
    """
    dataset = DataSet(str(input_dir))
    _sequence_id_list = sequence_id_list if sequence_id_list is not None else dataset.sequences(with_semseg=True)

    dataset_accessor = DataSetAccessor(dataset)

    data: list[dict[str, Any]] = []
    for sequence_id in _sequence_id_list:
        logger.debug(f"{sequence_id=} :: semsegのlabelごとの点の個数を取得します。")

        try:
            semseg_counts_list = dataset_accessor.get_semseg_counts_list(sequence_id)
            for semseg_counts in semseg_counts_list:
                tmp: dict[str, Any] = copy.deepcopy(semseg_counts.point_counts)
                tmp["frame_no"] = semseg_counts.frame_no
                tmp["sequence_id"] = semseg_counts.sequence_id
                data.append(tmp)
        except Exception:
            logger.warning(f"{sequence_id=} :: labelごとのsemsegの点の個数の取得に失敗しました。", exc_info=True)
            continue

    df = pandas.DataFrame(data)
    df = df.fillna(0)
    df = df.set_index(["sequence_id", "frame_no"])

    # columnを辞書順に並び替える
    df = df[sorted(df.columns)]
    renamed_target = {int(k): v for k, v in SEMSEG_CLASSES.items()}
    df.rename(columns=renamed_target, inplace=True)
    return df


def main() -> None:
    args = parse_args()
    set_logger()

    df = create_semseg_point_counts_dataframe(args.input_dir, args.sequence_id)
    output_file = args.output_csv
    output_file.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(str(output_file))


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description="semsegのclassごとの点数をCSV形式で出力します。",
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
