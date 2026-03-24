# MySQL — local: neeche values; live server: environment variables set karo
import os

MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', '786786'),
    'database': os.environ.get('MYSQL_DATABASE', 'cash_flow_app'),
    'port': int(os.environ.get('MYSQL_PORT', '3306')),
}
