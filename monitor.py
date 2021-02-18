from monitor_mysql import MysqlMonitor

if __name__ == '__main__':
    mysql = MysqlMonitor()
    mysql.monitor(whence=2)