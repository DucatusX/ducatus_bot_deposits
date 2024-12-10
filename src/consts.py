START_COMMAND = 'start'
BALANCE_COMMAND = 'balance'
STOP_COMMAND = 'stop'

TIMEOUT = 60
CONNECT_TIMEOUT = 30.0
READ_TIMEOUT = 60.0
WRITE_TIMEOUT = 60.0

REDIS_BALANCE_KEY = 'balance'
REDIS_CHAT_IDS_KEY = 'chat_ids'
REDIS_DATETIME_KEY = 'last_alert'
REDIS_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

NORMAL_LEVEL = {
    'high': 5_000_000,
    'low': 2_000_000,
    'time_delta': 15,
    'message': 'Withdrawal balance is low (less than 5 million). '
               'Please top up the balance. Current balance: {} {}'
}
MEDIUM_LEVEL = {
    'high': 2_000_000,
    'low': 100_000,
    'time_delta': 5,
    'message': 'Withdrawal balance is low (less than 2 million). '
               'Please top up the balance. Current balance: {} {}'
}
CRITICAL_LEVEL = {
    'high': 100_000,
    'low': 0,
    'time_delta': 2,
    'message': 'The balance for withdrawal is critically low (less than 100 thousand). '
               'Please top up the balance. Current balance: {} {}'
}
