import argparse
import logging
import shutil
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path

from pandaset import DataSet

from pandasetutils.common.pandaset import CameraType
from pandasetutils.common.utils import set_logger

logger = logging.getLogger(__name__)


def copy_camera_images(
    input_dir: Path,
    output_dir: Path,
    camera_type: CameraType,
    *,
    sequence_id_list: None | list[str] = None,
    frame_start: int = 0,
    frame_stop: int = 80,
    frame_step: int = 1,
) -> None:
    """
    指定したカメラの画像をコピーします。
    """
    dataset = DataSet(str(input_dir))
    _sequence_id_list = sequence_id_list if sequence_id_list is not None else dataset.sequences()

    target_frame_no_list = [f"{frame_no:02d}" for frame_no in range(frame_start, frame_stop, frame_step)]
    success_count = 0

    output_dir.mkdir(exist_ok=True, parents=True)
    for sequence_id in _sequence_id_list:
        camera_dir = input_dir / sequence_id / "camera" / camera_type.value
        for frame_no in target_frame_no_list:
            original_first_frame_filename = f"{frame_no}.jpg"
            original_image_file = camera_dir / original_first_frame_filename
            if not original_image_file.exists():
                logger.warning(f"'{original_image_file}'は存在しません。ファイルのコピーをスキップします。")
                continue

            output_file = output_dir / f"{sequence_id}__{camera_type.value}__{frame_no}.jpg"

            try:
                shutil.copy(original_image_file, output_file)
                success_count += 1
            except Exception:
                logger.warning(f"{original_image_file}のファイルコピーに失敗しました。", exc_info=True)

    logger.info(f"{success_count} 件の'{camera_type.value}'の画像ファイルを'{output_dir}'にコピーしました。")


def main() -> None:
    args = parse_args()
    set_logger()

    copy_camera_images(
        args.input_dir,
        args.output_dir,
        camera_type=CameraType(args.camera),
        sequence_id_list=args.sequence_id,
        frame_start=args.frame_start,
        frame_stop=args.frame_stop,
        frame_step=args.frame_step,
    )


def parse_args() -> argparse.Namespace:
    parser = ArgumentParser(
        description=(
            "データセットから指定したカメラ画像の`00.jpg`を別のディレクトリにコピーします。コピー後のファイル名は`{sequence_id}__{camera}_00.jpg`です。"
        ),
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_dir", type=Path, help="pandasetのディレクトリ")
    parser.add_argument("output_dir", type=Path, help="出力先ディレクトリ")
    parser.add_argument("--camera", type=str, choices=[e.value for e in CameraType], required=True, help="コピー対象のcameraの種類")

    parser.add_argument("--sequence_id", type=str, nargs="+", required=False, help="出力対象のsequence id")

    parser.add_argument("--frame_start", default=0, type=int, help="コピー対象のフレームの開始位置")
    parser.add_argument("--frame_stop", default=80, type=int,help="コピー対象のフレームの終了位置（ただし含まない）")
    parser.add_argument("--frame_step", default=1, type=int, help="コピー対象のフレームの増分")

    return parser.parse_args()


if __name__ == "__main__":
    main()
