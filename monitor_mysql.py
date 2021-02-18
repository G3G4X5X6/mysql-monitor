import pymysql


class DbBase(object):
    """
    数据库接口类
    """
    # MySQL数据库配置
    HOST = "127.0.0.1"
    PORT = 3306
    DATABASE = "information_schema"
    USERNAME = "root"
    PASSWORD = "123456"
    CHARSET = 'utf8'

    def follow(self, file, whence=2):
        # file.seek(off, whence=0)
        # off: 正数往结束方向移动，负数往开始方向移动
        # whence: 0代表从头开始， 1代表当前位置， 2代表文件最末尾位置
        file.seek(0, whence)
        while True:
            log_lines = file.readline()
            if not log_lines:
                # 此处可设置查询频率
                # import time
                # time.sleep(0.1)
                continue
            yield log_lines

    def exec(self, sql):
        pass

    def monitor(self, whence=2):
        pass


class MysqlBase(DbBase):
    """
    Mysql通用配置基类
    """
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
    SET_GENERAL_LOG_FILE = "set global general_log_file='"


class MysqlMonitor(MysqlBase):
    """
    Mysql查询日志实时监控实现类
    """
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(host=self.HOST,
                                          port=self.PORT,
                                          user=self.USERNAME,
                                          password=self.PASSWORD,
                                          database=self.DATABASE,
                                          charset=self.CHARSET)

    def exec(self, sql):
        """
        执行sql语句
        :param sql: Mysql查询语句
        :return: fetchall
        """
        try:
            with self.connection.cursor() as cursor:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交事务
                self.connection.commit()

                return cursor.fetchall()
            print("Cursor Error!")
        except pymysql.DatabaseError:

            self.connection.rollback()  # 数据库事务回滚
            print("Error!")
        finally:
            pass

    def monitor(self, whence=2):
        """
        Mysql查询日志实时监控
        :param whence: 定义日志文件起始读取位置
        :return: None
        """
        log_path = self.exec(self.SHOW_GENERAL_LOG_STATUS)[1][1]
        if self.exec(self.SHOW_GENERAL_LOG_STATUS)[0][1] == 'OFF':
            print("The options status: ('general_log', 'OFF')")
            print("开启查询日志......")
            self.set_log_on()
        for tp in mysql.get_general_log_status():
            print(tp)
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = self.follow(f, whence=whence)
                for line in lines:
                    print(line, end='')
        except KeyboardInterrupt:
            self.close()
            print(KeyboardInterrupt.__name__ + ": Ctrl+C")

    def get_log_status(self):
        """
        查看MySQL日志相关设置状态
        :return: tuple
        """
        return self.exec(self.SHOW_LOG_CONFIG)

    def get_general_log_status(self):
        """
        查看Mysql查询日志general_log设置状态
        :return: tuple
        """
        return self.exec(self.SHOW_GENERAL_LOG_STATUS)

    def set_log_on(self):
        """
        开启Mysql查询日志 general_log
        :return: None
        """
        self.exec(self.SET_GENERAL_LOG_ON)
        self.get_general_log_status()

    def set_log_off(self):
        """
        关闭Mysql查询日志 general_log
        :return: None
        """
        self.exec(self.SET_GENERAL_LOG_OFF)
        self.get_general_log_status()

    def set_log_file(self, filepath):
        """
        设置Mysql查询日志文件输出路径 general_log_file
        :param filepath:
        :return: None
        """
        self.exec(self.SET_GENERAL_LOG_FILE + filepath + "'")

    def close(self):
        """
        关闭Mysql连接
        :return: None
        """
        self.connection.close()


if __name__ == '__main__':
    mysql = MysqlMonitor()
    mysql.monitor()
    mysql.close()

"""
pymysql.Connect()参数说明
host(str):      MySQL服务器地址
port(int):      MySQL服务器端口号
user(str):      用户名
passwd(str):    密码
db(str):        数据库名称
charset(str):   连接编码

connection对象支持的方法
cursor()        使用该连接创建并返回游标
commit()        提交当前事务
rollback()      回滚当前事务
close()         关闭连接

cursor对象支持的方法
execute(op)     执行一个数据库的查询命令
fetchone()      取得结果集的下一行
fetchmany(size) 获取结果集的下几行
fetchall()      获取结果集中的所有行
rowcount()      返回数据条数或影响行数
close()         关闭游标对象
"""
