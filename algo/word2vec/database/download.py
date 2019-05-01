import MySQLdb
import re
import jieba
import config


def downlaod():
    try:
        conn = MySQLdb.connect(host=config.DATABASE_CONFIG['host'],
                               port=config.DATABASE_CONFIG['port'],
                               db=config.DATABASE_CONFIG['db'],
                               user=config.DATABASE_CONFIG['user'],
                               passwd=config.DATABASE_CONFIG['passwd'],
                               charset=config.DATABASE_CONFIG['charset'])

        cursor = conn.cursor()
        cursor.execute("SELECT content FROM news_chinese.sqlResult_1558435")
        content = cursor.fetchall()
        cut_to_words(content)

    except MySQLdb.Error as e:
        print("connect mysql error {}".format(e))

    finally:
        if conn:
            conn.close()
            print("mysql connection is closed")


def remove_extra_char(string):
    pattern = re.compile('[\w|\d]+')
    string = pattern.findall(str(string))
    return ' '.join(s for s in string)


def cut_to_words(contents):
    text = [remove_extra_char(t) for t in contents]
    text = ''.join(t for t in text)
    words = list(jieba.cut(text))
    tokens = [t for t in words if t.strip() and t != 'n']

    with open("database_news.txt", 'w') as fw:
        for t in tokens:
            fw.write(t)
            fw.write(' ')


downlaod()