# Описание тестов для shh и nginx

Настройка linux выполнялась следующим образом:
1. В конфигах sshd и nginx порты изменены на 8015 и 5478 соответственно
2. Выполнены команды для firewalld:
    - firewall-cmd --permanent --add-service=http //добавление сервиса http
    - firewall-cmd --permanent --add-service=ssh //добавление сервиса ssh
    - firewall-cmd --permanent --add-port=8015/tcp
    - firewall-cmd --permanent --add-port=5478/tcp //разрешение портов 8015
    - firewall-cmd --reload //перезагрузка firewalld демона
3. Выполнены команды для selinux:
    - semanage port -a -t http_port_t -p tcp 5478 //разрешаем порт для nginx
    - semanage port -a -t sshd_port_t -p tcp 8015 //разрешаем порт для sshd
    
Таким образом у нас поднимаются sshd и nginx демоны на недефолтных портах.

Для pytest сущестуют следующие аргументы:
- --host: хост, на котором запущен сервер
- --port: порт, на котором запущен sshd
- --nginx-port: порт, на котором запущен nginx

В качестве пользователя для centos всегда используется root (с паролем root).