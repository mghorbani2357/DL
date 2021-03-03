#!/usr/bin/python
import sqlite3
from typing import Union


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def normalize(var, string_symbol: str = '"'):
    if isinstance(var, (int, float)):
        return str(var)
    elif isinstance(var, bool):
        return 'true' if var else 'false'
    else:
        return '%s%s%s' % (string_symbol, var, string_symbol)


def normalize_for_sql(items: [Union[list, set, tuple]], string_symbol: str = '"'):
    temp = []
    for i in items:
        temp.append(normalize(i, string_symbol))
    return temp


def where_normalize(conditions: [Union[dict, bool]]):
    temp = []
    if isinstance(conditions, bool):
        temp = normalize(conditions)
    else:
        for k, v in conditions.items():
            if isinstance(v, dict):
                temp.append(where_normalize(v))
            elif isinstance(v, (list, tuple, set)):
                temp2 = []
                for k2 in v:
                    temp2.append('%s=%s' % (normalize(k, '`'), normalize(k2)))
                temp.append('(%s)' % (' OR '.join(temp2)))

            else:
                temp.append('%s=%s' % (normalize(k, '`'), normalize(v)))
        temp = ' AND '.join(temp)
    return temp


class DBManager:
    def __init__(self, db_name):
        conn = None
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            if len(cursor.fetchall()) == 0:
                with open('structure.sql', 'r') as structure:
                    conn.executescript(structure.read())
                    conn.commit()
            else:
                with open('migration.sql', 'r') as structure:
                    conn.executescript(structure.read())
                    conn.commit()
            # print(len(cursor.fetchall()))
            self.db = db_name
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def execute(self):
        pass

    def insert(self, table: str, item: [Union[dict, str]]):
        if isinstance(item, str):
            sql = item
        else:
            sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, ', '.join(normalize_for_sql(item.keys(), '`')), ', '.join(normalize_for_sql(item.values())))
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def update(self, table: str, item: [Union[dict, str]], where: [Union[dict, bool, str]]):
        if isinstance(item, str):
            sql = item
        else:
            temp = []
            for k, v in item.items():
                temp.append('%s=%s' % (normalize(k, '`'), normalize(v)))
            ','.join(temp)
            if not isinstance(where, str):
                where = where_normalize(where)
            sql = "UPDATE %s SET %s WHERE %s" % (table, temp, where)

        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def delete(self, table: str, where: [Union[dict, bool, str]]):
        if isinstance(where, str):
            sql = where
        else:
            sql = "DELETE FROM `%s` WHERE %s" % (table, where_normalize(where))
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()
        conn.close()

    def select(self, table: str, cols: [Union[str, list, set, tuple]], where: [Union[dict, bool, str, None]] = None):
        if isinstance(cols, str) and cols.strip() != "*":
            sql = cols
        else:
            if not isinstance(cols, str):
                cols = ",".join(normalize_for_sql(cols, '`'))
            sql = "SELECT %s FROM `%s` %s" % (cols, table, '' if where is None else "WHERE %s" % where_normalize(where))

        conn = sqlite3.connect(self.db)
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        conn.close()
        return data

# def create(self, sql):
#     conn = sqlite3.connect(self.db)
#     conn.execute(sql)
#     conn.commit()
# def update(self, sql):
#     self.create()
