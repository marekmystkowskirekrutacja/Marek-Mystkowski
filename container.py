import sqlite3

class Container:
  __database = ''
  
  def __init__(self, database = 'database.db'):
    self.__database = database
    self.__execute('CREATE TABLE IF NOT EXISTS objects (key text, data text, type text)')

  def __execute(self, sql, param = [], function = lambda x: x):
    conn = sqlite3.connect(self.__database)
    c = conn.cursor()
    result = function(c.execute(sql, param))
    conn.commit()
    conn.close()
    return result
  
  def get_all(self):
    return self.__execute('SELECT key FROM objects', function = lambda rows: list(map(lambda row: row[0], rows)))
  
  def get(self, key):
   rows = self.__execute(
      'SELECT data, type FROM objects WHERE key = ? LIMIT 1',
      param = (key,),
      function = lambda rows: list(map(lambda row: {'content' : row[0], 'type' : row[1]}, rows))
     )
   if len(rows) == 0:
     raise KeyError()
   return rows[0]
  
  def add(self, key, value, type):
    self.delete(key)
    self.__execute('INSERT INTO objects VALUES (?,?,?)', param = (key, value, type))
    
  def delete(self, key):
    self.__execute('DELETE FROM objects WHERE key = ?', param = (key,))