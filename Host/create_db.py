"""Database + table create — ek baar chalao: python create_db.py"""
import mysql.connector
from mysql.connector import Error

from config import MYSQL_CONFIG

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS cash_flow_snapshot (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  snapshot_key VARCHAR(64) NOT NULL DEFAULT 'default',
  payload JSON NOT NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_snapshot_key (snapshot_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


def main():
    cfg = MYSQL_CONFIG.copy()
    db_name = cfg.pop('database')
    try:
        conn = mysql.connector.connect(**cfg)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cur.close()
        conn.close()

        cfg['database'] = db_name
        conn = mysql.connector.connect(**cfg)
        cur = conn.cursor()
        cur.execute(CREATE_TABLE)
        conn.commit()
        cur.close()
        conn.close()
        print(f"OK: database '{db_name}' + table 'cash_flow_snapshot' ready.")
    except Error as e:
        print("MySQL Error:", e)
        raise


if __name__ == '__main__':
    main()
