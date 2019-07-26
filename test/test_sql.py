from handle_mysql import MySQL
mysql = MySQL()
try:

    mysql.get_connection()
    mysql.insert('tb_column',)

    # column = mysql.select('tb_column', ['column_id', 'current_article_num'], 'column_name="%s"' % '万维钢·精英日课³')
    # # print(result)
    #
    # crawled_article = []
    #
    # # 如果数据库中有
    # if column:
    #     column_id = column[0][0]
    #     current_article_num = column[0][1]
    #     print(column_id, current_article_num)
    #
    #
    #     def f(x):
    #         return x[0]
    #
    #
    #     crawled_article_id = mysql.select('article_column', ['article_id'], 'column_id="%s"' % column_id)
    #     crawled_article_ids = list(map(f, crawled_article_id))
    #     print(crawled_article_ids)
    #     print(len(crawled_article_ids), current_article_num)
    #     # if len(crawled_article_ids) < current_article_num:
    #     for article_id in crawled_article_ids:
    #         article_name = mysql.select('article', ['article_name'], 'article_id="%s"' % article_id)
    #         article_name = article_name[0][0]
    #         crawled_article.append(article_name)
    #         print(article_name)
    #     print(crawled_article)

finally:

    mysql.close_connection()
