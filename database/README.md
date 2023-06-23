
### cuboid_count_by_label.csv
cuboidのlabelごとのオブジェクト数


### semseg_point_count_by_class.csv
semsegのclassごとの点の個数。
※ なぜかclassが'0'のものがありました。
https://github.com/scaleapi/pandaset-devkit/issues/132

以下、classのIDとNAMEの関係です。

```
{
 '1': 'Smoke',
 '2': 'Exhaust',
 '3': 'Spray or rain',
 '4': 'Reflection',
 '5': 'Vegetation',
 '6': 'Ground',
 '7': 'Road',
 '8': 'Lane Line Marking',
 '9': 'Stop Line Marking',
 '10': 'Other Road Marking',
 '11': 'Sidewalk',
 '12': 'Driveway',
 '13': 'Car',
 '14': 'Pickup Truck',
 '15': 'Medium-sized Truck',
 '16': 'Semi-truck',
 '17': 'Towed Object',
 '18': 'Motorcycle',
 '19': 'Other Vehicle - Construction Vehicle',
 '20': 'Other Vehicle - Uncommon',
 '21': 'Other Vehicle - Pedicab',
 '22': 'Emergency Vehicle',
 '23': 'Bus',
 '24': 'Personal Mobility Device',
 '25': 'Motorized Scooter',
 '26': 'Bicycle',
 '27': 'Train',
 '28': 'Trolley',
 '29': 'Tram / Subway',
 '30': 'Pedestrian',
 '31': 'Pedestrian with Object',
 '32': 'Animals - Bird',
 '33': 'Animals - Other',
 '34': 'Pylons',
 '35': 'Road Barriers',
 '36': 'Signs',
 '37': 'Cones',
 '38': 'Construction Signs',
 '39': 'Temporary Construction Barriers',
 '40': 'Rolling Containers',
 '41': 'Building',
 '42': 'Other Static Object'
}
```