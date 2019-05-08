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

    text = []
    for content in contents:
        for con in content:
            text += [c for c in re.split("。|？|！", con) if c != '']

    pattern = re.compile('[\w|\d]+')
    text = [''.join(pattern.findall(t)) for t in text]

    jieba.enable_parallel(3)
    words = [list(jieba.cut(t)) for t in text]

    with open("database_news.txt", 'w') as fw:
        for word in words:
            if len(word) <= 0:
                continue
            for w in word:
                fw.write(w + ' ')
            fw.write('\n')


downlaod()