from news import settings
import pymysql
db = pymysql.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'],
                     settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'], charset='utf8mb4')
cursor = db.cursor()


# def init_admin_user():
#     INSERT_SQL = '''
#                 INSERT INTO T_USER(USER_EMAIL,) VALUES(%d,'%s');
#                 ''' % (city['cityId'], city['cityName'])
#     cursor.execute(INSERT_SQL)
#     db.commit()
#     print('初始化管理员完成')


# if __name__ == "__main__":
# init_admin_user()
