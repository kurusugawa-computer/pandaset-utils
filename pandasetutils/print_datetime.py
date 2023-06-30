import argparse
import datetime
import json
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path
from typing import Any

import pandas
from pandaset import DataSet

from pandasetutils.common.utils import set_logger

logger = logging.getLogger(__name__)


def get_datetime_from_json(timestamps_json: Path) -> str:
    """
    `timestamps.json`に記載されている先頭のtimestampからISO8601形式の文字列を取得します。
    """
    with timestamps_json.open() as f:
        data = json.load(f)
    first_timestamp = data[0]
    first_datetime = datetime.datetime.fromtimestamp(first_timestamp)  # noqa: DTZ006
    return first_datetime.isoformat()


def create_cuboid_counts_dataframe(input_dir: Path, sequence_id_list: None | list[str] = None) -> pandas.DataFrame:
    """
    シーケンスごとのtimestamp(ISO8601形式)が格納された`pandas.DataFrame`を生成します。

    Args:
        input_dir: pandasetのディレクトリ
        sequence_id_list: 取得対象のsequence_idのlist。Noneならば全てのsequence_idが取得対象になります。
    Returns:
        index: sequence_id
        columns: cuboidのlabel
    """
    dataset = DataSet(str(input_dir))
    _sequence_id_list = sequence_id_list if sequence_id_list is not None else dataset.sequences()

    data: list[dict[str, Any]] = []
    for sequence_id in _sequence_id_list:
        logger.info(f"{sequence_id=}のsemsegのtimestamp情報を取得します。")
        try:
            str_datetime = get_datetime_from_json(input_dir / sequence_id / "meta/timestamps.json")

            data.append({"sequence_id": sequence_id, "datetime": str_datetime})

        except Exception:
            logger.warning(f"{sequence_id=}の`timestamps.json`のロードに失敗しました。", exc_info=True)
        finally:
            dataset.unload(sequence_id)

    df = pandas.DataFrame(data)
    df.fillna(0, inplace=True)
    return df


def main() -> None:
    args = parse_args()
    set_logger()

    df = create_cuboid_counts_dataframe(args.input_dir, sequence_id_list=args.sequence_id)
    output_csv_file: Path = args.output_csv
    output_csv_file.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(str(output_csv_file), index=False)


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description="各シーケンスのtimestampをISO形式で出力します。",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_dir", type=Path, help="pandasetのディレクトリ")
    parser.add_argument("output_csv", type=Path, help="CSVファイルの出力先")
    parser.add_argument("--sequence_id", type=str, nargs="+", required=False, help="出力対象のsequence id")

    return parser.parse_args()


if __name__ == "__main__":
    main()
