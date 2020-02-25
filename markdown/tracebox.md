# Tracebox

[call table](/tdg/data_dumps/tracebox_2nd/parquets/CALL_20180628) : 186 columns

|variable|desc|comments|
|_______|________|________|
|`POS_*_*`|x,y first/last position| 11 cm precision|
|`*_TIME`| start/end time, seconds|from UTC|
|`M_TMSI`|temporary imsi hash|ex: F88D6A78| 
|`S_TMSI`|temporary imsi hash|ex: 70-F88D6A78| 
|`TAC`| device identifier||
|`MCC`| country code||
|`MNC`| country + operator code||
|`POS_*_TILE`||

95% of the records do not show any movement.

![tracebox_pos](../f/f_prod/tracebox_pos.png "tracebox position")
_tracebox positions_

