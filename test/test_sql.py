from handle_mysql import MySQL
mysql = MySQL()
mysql.get_connection()
def f(x):
    return x[0]

result = mysql.select('tb_column', ['column_name'], 'crawl_finished = 1')

print(result)
print(list(map(f,result)))
mysql.close_connection()
