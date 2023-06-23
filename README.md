# pandaset-utils

## Scripts

### cuboidのラベルごとのオブジェクト数を算出

```
$ poetry run python -m pandaset_utils.pandasetutils.print_cuboid_count ${INPUT_DIR} ${OUTPUT_CSV}
```

出力結果（CSV）は以下を参照してください。
https://github.com/kurusugawa-computer/pandaset-utils/blob/main/database/cuboid_count_by_label.csv

### semsegのクラスごとの点の個数を算出

```
$ poetry run python -m pandaset_utils.pandasetutils.print_semseg_point_count ${INPUT_DIR} ${OUTPUT_CSV}
```

出力結果（CSV）は以下を参照してください。
https://github.com/kurusugawa-computer/pandaset-utils/blob/main/database/semseg_point_count_by_class.csv
