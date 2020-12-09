#
#  1. 运动健康数据自动生成的配置文件
#  值的范围控制在合理范围之内。不做非法数据的测试
#

TRANSLATE_TYPE_SPORT = '1'

TRANSLATE_TYPE_HEALTH = '2'

TRANSLATE_TYPE_HEALTH_SLEEP = '3'

TRANSLATE_TYPE_HEALTH_SPO = '4'

TRANSLATE_TYPE_EVENTPOINT = '5'


# 1. 运动数据
SPORT_VERSION =  1         # 版本号
# 运动类型范围，参考代码 dualcom.pb.h中的定义
SPORT_TYPE_MIN = 0         # 运动类型最小值
SPORT_TYPE_MAX = 114       # 运动类型最大值
# 需要自动生成的数据的时间戳的范围。 最大距离当前时间30天内的数据，超过不会同步到手机
SPORT_TIMESTAMP_MAX_DAY = 30
SPORT_TIMESTAMP_END     = '2011-11-04 00:05:23'

# 单次运动的距离范围. 单位公里
SPORT_DISTANCE_MIN   = 0.2
SPORT_DISTANCE_MAX   = 50

# 每公里的用时范围。 单位秒
SPORT_TIME_PER_KM_MIN   = 30
SPORT_TIME_PER_KM_MAX  =  600

# 完成度范围
SPORT_FINISH_MIN = 0
SPORT_FINISH_MAX = 100

# 体能等级范围
SPORT_STAMINALEVEL_MIN = 0
SPORT_STAMINALEVEL_MAX = 10

# 最大心率范围
SPORT_HEARTRATE_MIN = 10
SPORT_HEARTRATE_MIN = 200

# 卡路里范围
SPORT_CALORIES_MIN = 10
SPORT_CALORIES_MAX = 200

# 心率五区间的时间范围. 单位 秒
SPORT_HRZONE_MIN  = 10
SPORT_HRZONE_MAX  = 300

# 体能的范围
SPORT_STAMINA_MIN  = 10
SPORT_STAMINA_MAX  = 100

# 配速
SPORT_PACE_MIN  = 10
SPORT_PACE_MAX  = 100

# 海拔
SPORT_LATITUDE_MIN  = 10
SPORT_LATITUDE_MAX  = 100

# 高度
SPORT_HEIGHT_MIN  = 10
SPORT_HEIGHT_MAX  = 100

# 步数
SPORT_STEP_MIN = 0
SPORT_STEP_MAX = 500

# 血氧
SPORT_SPO_MIN = 0
SPORT_SPO_MAX = 100

# 配速
SPORT_SPEED_MIN = 0
SPORT_SPEED_MAX = 100

# 运动状态
SPORT_STATUS_MIN = 0
SPORT_STATUS_MAX = 10

# 1.1 非游泳运动
# 1.1.2 运动记录


# 1.1.3 运动报告
SPORT_AUTO_FLAG_MIN   = 0
SPORT_AUTO_FLAG_MAX   = 1


# 1.2 游泳运动
# 1.2.1 索引文件
# 1.2.2 运动记录
# 1.2.3 运动报告

# 2. 健康数据
# 2.1 每日活动，心率，静息心率，压力

# 2.2 睡眠

# 2.3 血氧
# 2.3.1 索引文件
# 血氧测试的时间范围。 单位 秒
HEALTH_SPO_NORMAL_TIME_MIN  = 30
HEALTH_SPO_NORMAL_TIME_MAX  = 30*60

HEALTH_SPO_SLEEP_TIME_MIN  = 30*60
HEALTH_SPO_SLEEP_TIME_MAX  = 8*60*60

# 睡眠血氧和普通血氧。  255 是普通血氧  其他都是睡眠血氧
HEALTH_SPO_TYPE_MIN  = 254
HEALTH_SPO_TYPE_MAX  = 255

# 血氧时间范围不要超过距离当前时间 30 天。 超过 30 天的数据不会被同步到手机
HEALTH_TIMESTAMP_MAX_DAY = 30
HEALTH_TIMESTAMP_END     = '2020-10-9 20:40:00'

# 血氧记录之间的休息时间。 单位 秒
HEALTH_SPO_GAP_TIME_MIN = 30
HEALTH_SPO_GAP_TIME_MAX = 300

# 血氧数据文件的版本号
HEALTH_SPO_DATA_VERSION_NUM = 'v0'
HEALTH_SPO_FILE_EXT         = '.spo'
HEALTH_SPO_INDEX_EXT = 'index1.spo'

# 2.3.2 数据文件
HEALTH_SPO2_MIN  = 20
HEALTH_SPO2_MAX   = 100




# 3. 埋点事件
# 1个埋点文件中的埋点个数
EP_TIMESTAMP_MAX_COUNT = 500
EP_TIMESTAMP_DAY       =  3
EP_TIMESTAMP_END     = '2020-09-27 10:20:00'

EP_DATA_GAP_TIME_MIN = 30
EP_DATA_GAP_TIME_MAX = 60

EP_ONE_FILE_TIME_MIN = 500
EP_ONE_FILE_TIME_MAX = 700

# 3.1 索引
# 3.2 数据文件


