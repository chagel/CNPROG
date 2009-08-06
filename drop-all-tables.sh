mysql_username='cnprog'
mysql_database='cnprog'
mysqldump -u $mysql_username -p --add-drop-table --no-data $mysql_database | grep ^DROP 
#| mysql -u[USERNAME] -p[PASSWORD] [DATABASE]
