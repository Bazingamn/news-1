# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TBrowseRec(models.Model):
    browse_id = models.AutoField(db_column='BROWSE_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('TUser', models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    news_id = models.BigIntegerField(db_column='NEWS_ID')  # Field name made lowercase.
    browse_time = models.DateTimeField(db_column='BROWSE_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_BROWSE_REC'


class TCollection(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING, db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    news_id = models.BigIntegerField(db_column='NEWS_ID')  # Field name made lowercase.
    collect_time = models.DateTimeField(db_column='COLLECT_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_COLLECTION'
        unique_together = (('user', 'news_id'),)


class TComment(models.Model):
    comment_id = models.AutoField(db_column='COMMENT_ID', primary_key=True)  # Field name made lowercase.
    news_id = models.BigIntegerField(db_column='NEWS_ID')  # Field name made lowercase.
    user = models.ForeignKey('TUser', models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    comment_time = models.DateTimeField(db_column='COMMENT_TIME')  # Field name made lowercase.
    comment_text = models.CharField(db_column='COMMENT_TEXT', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_COMMENT'


class TRecommend(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING, db_column='user', primary_key=True)
    product = models.BigIntegerField()
    rating = models.DecimalField(max_digits=17, decimal_places=16)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'T_RECOMMEND'
        unique_together = (('user', 'product'),)


class TSearchRec(models.Model):
    search_id = models.AutoField(db_column='SEARCH_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('TUser', models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    keyword = models.CharField(db_column='KEYWORD', max_length=50)  # Field name made lowercase.
    search_time = models.DateTimeField(db_column='SEARCH_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_SEARCH_REC'


class TUser(models.Model):
    user_id = models.AutoField(db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    sign_up_time = models.DateTimeField(db_column='SIGN_UP_TIME')  # Field name made lowercase.
    user_email = models.CharField(db_column='USER_EMAIL', max_length=100)  # Field name made lowercase.
    user_passwd = models.CharField(db_column='USER_PASSWD', max_length=100)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50)  # Field name made lowercase.
    user_avatar_url = models.CharField(db_column='USER_AVATAR_URL', max_length=500)  # Field name made lowercase.
    user_gender = models.IntegerField(db_column='USER_GENDER', blank=True, null=True)  # Field name made lowercase.
    user_birth = models.DateField(db_column='USER_BIRTH', blank=True, null=True)  # Field name made lowercase.
    user_location = models.CharField(db_column='USER_LOCATION', max_length=50)  # Field name made lowercase.
    user_introduce = models.CharField(db_column='USER_INTRODUCE', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_USER'
        unique_together = (('user_id', 'user_email'),)


class TUseRec(models.Model):
    use_id = models.AutoField(db_column='USE_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(TUser, models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    use_time = models.DateTimeField(db_column='USE_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_USE_REC'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class NewsCacheBackstageTask(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_cache_backstage_task'


class NewsCacheContUrl(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_cache_cont_url'


class NewsCacheLevelUrl(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_cache_level_url'


class NewsCacheLogin(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_cache_login'


class NewsCacheSourceUrl(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_cache_source_url'


class NewsCollected(models.Model):
    url = models.CharField(max_length=1000)
    urlmd5 = models.CharField(db_column='urlMd5', max_length=32)  # Field name made lowercase.
    release = models.CharField(max_length=10)
    task_id = models.IntegerField()
    target = models.CharField(max_length=1000)
    desc = models.CharField(max_length=1000)
    error = models.CharField(max_length=1000)
    addtime = models.IntegerField()
    titlemd5 = models.CharField(db_column='titleMd5', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'news_collected'


class NewsCollector(models.Model):
    task_id = models.IntegerField()
    name = models.CharField(max_length=50)
    module = models.CharField(max_length=10)
    addtime = models.IntegerField()
    uptime = models.IntegerField()
    config = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_collector'


class NewsConfig(models.Model):
    cname = models.CharField(primary_key=True, max_length=32)
    ctype = models.PositiveIntegerField()
    dateline = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'news_config'


class NewsProxyIp(models.Model):
    ip = models.CharField(primary_key=True, max_length=100)
    user = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    invalid = models.IntegerField()
    failed = models.IntegerField()
    num = models.IntegerField()
    time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_proxy_ip'


class NewsRelease(models.Model):
    task_id = models.IntegerField()
    name = models.CharField(max_length=50)
    module = models.CharField(max_length=10)
    addtime = models.IntegerField()
    config = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_release'


class NewsReleaseApp(models.Model):
    module = models.CharField(max_length=10)
    app = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    addtime = models.IntegerField()
    uptime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_release_app'
        unique_together = (('module', 'app'),)


class NewsRule(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    module = models.CharField(max_length=20)
    store_id = models.IntegerField()
    addtime = models.IntegerField()
    uptime = models.IntegerField()
    config = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_rule'


class NewsTask(models.Model):
    name = models.CharField(max_length=50)
    tg_id = models.IntegerField()
    module = models.CharField(max_length=10)
    auto = models.IntegerField()
    sort = models.IntegerField()
    addtime = models.IntegerField()
    caijitime = models.IntegerField()
    config = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_task'


class NewsTaskgroup(models.Model):
    name = models.CharField(max_length=50)
    parent_id = models.IntegerField()
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_taskgroup'


class NewsUser(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    groupid = models.IntegerField()
    email = models.CharField(max_length=255)
    regtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_user'


class NewsUsergroup(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    founder = models.IntegerField()
    admin = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_usergroup'
