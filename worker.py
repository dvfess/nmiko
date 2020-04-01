#!/usr/bin/env python3
# -*- coding: utf-*-
from netmiko import ConnectHandler


def main(ip, user, passwd, cliLogger):

    # Массив для хранения результата
    results = []
    commands = [
        'show log messages | match "Failed to allocate"',
        'show log messages.0.gz | match "Failed to allocate"',
        'show log messages.1.gz | match "Failed to allocate"',
        'show log messages.2.gz | match "Failed to allocate"',
        'show log messages.3.gz | match "Failed to allocate"',
        'show log messages.4.gz | match "Failed to allocate"',
        'show log messages.5.gz | match "Failed to allocate"',
        'show log messages.6.gz | match "Failed to allocate"',
        'show log messages.7.gz | match "Failed to allocate"',
        'show log messages.8.gz | match "Failed to allocate"',
        'show log messages.9.gz | match "Failed to allocate"',
    ]

    def strFilter(line):
        '''Функция, для фильрации набора строк в логах'''
        # # Ищем следующие строки
        sequence = ('CHASSISD_TEMP_HOT_NOTICE',
                    'CHASSISD_ZONE_BLOWERS_SPEED_FULL',
                    'CHASSISD_IFDEV_DETACH_PIC')
        for item in sequence:
            if item in line:
                return True

    cliLogger.info('CONNECTION TO DEVICE {}'.format(ip))

    try:
        DEVICE_PARAMS = {'device_type': 'juniper_junos',
                         'ip': ip,
                         'username': user,
                         'password': passwd,
                         'verbose': True}

        with ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()
            hostname = ssh.find_prompt()
            for cmd in commands:
                results.append(ssh.send_command(cmd))
                print(len(results))

    except Exception as e:
        cliLogger.warning('CONNECTION TO DEVICE FAILS {} ({})'.format(ip, e))
        return ''

    # Отправим, в качестве результата
    logBuffer = ''

    logBuffer += hostname+'\n'

    # ФИЛЬТРАЦИЯ ЛОГОВ ЧЕРЕЗ ФУНКЦИЮ ФИЛЬТРАЦИИ
    # Если нужно несколько фильтров. Больше применимо к цискам.
    for messages in results:
        # Фильтруем сообщения только по интересующим строкам
        filtered = list(filter(strFilter, messages.splitlines()))
        for line in filtered:
            logBuffer += line + '\n'

    # # Тупой сбор логов. Если нужна фильтрация, указывается в команде
    # for messages in results:
    #     logBuffer += messages

    return logBuffer


if __name__ == '__main__':
    main()
