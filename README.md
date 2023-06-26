# pandaset-utils

## Scripts

### cuboidのラベルごとのオブジェクト数を算出

```
$ poetry run python -m pandasetutils.print_cuboid_count ${INPUT_DIR} ${OUTPUT_CSV}
```

出力結果（CSV）は以下を参照してください。
https://github.com/kurusugawa-computer/pandaset-utils/blob/main/database/cuboid_count_by_label.csv

### semsegのクラスごとの点の個数を算出

```
$ poetry run python -m pandasetutils.print_semseg_point_count ${INPUT_DIR} ${OUTPUT_CSV}
```

出力結果（CSV）は以下を参照してください。
https://github.com/kurusugawa-computer/pandaset-utils/blob/main/database/semseg_point_count_by_class.csv


### シーケンスごとのdatetimeを出力


```
$ poetry run python -m pandasetutils.print_datetime ${INPUT_DIR} ${OUTPUT_CSV}
```

出力結果（CSV）は以下を参照してください。
https://github.com/kurusugawa-computer/pandaset-utils/blob/main/database/datetime.csv



### 指定したカメラ画像を別のディレクトリにコピー

指定したカメラ画像を別のディレクトリにコピーします。コピー後のファイル名は`{sequence_id}__{camera}__{frame_no}.jpg`です。

```
$ poetry run python -m pandasetutils.copy_camera_image ${INPUT_DIR} ${OUTPUT_DIR} --camera front_camera

$ ls -1 ${OUTPUT_DIR}
001__front_caamera__00.jpg
001__front_caamera__10.jpg
...
```

