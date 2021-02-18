"""

"""


class Config(object):
    # 查看日志相关配置信息
    SHOW_LOG_CONFIG = "show variables like '%log%'"
    # ON开启日志，OFF关闭日志，默认好像是关闭的
    SHOW_GENERAL_LOG_STATUS = "show variables like '%general_log%'"
    # TABLE: 日志输出到表mysql.general_log中，FILE: 日志输出到general_log变量指向的文件中
    SHOW_LOG_OUTPUT_STATUS = "show variables like '%log_output%'"
    # 是否开启了慢日志，这个好像需要通过修改配置文件并重启SQL服务才可以
    SHOW_SLOW_QUERY_STATUS = "show variables like '%slow_query%'"

    # 将日志输出到mysql.general_log中，在很多操作后，查看日志查不出来，太慢了
    SET_LOG_OUTPUT_TO_TABLE = "set global log_output = 'TABLE'"
    # 打开日志记录
    SET_GENERAL_LOG_ON = "set global general_log = 'ON'"
    # 关闭日志记录
    SET_GENERAL_LOG_OFF = "set global general_log = 'OFF'"
    # 设置General log的日志文件路径
    SET_GENERAL_LOG_FILE = "set global general_log_file='/var/mysql/data/query.log'"
