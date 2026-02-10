#!/bin/bash

# Цвета для вывода, чтобы в терминале VS Code было красиво
GREEN='\033[0-32m'
NC='\033[0m' # No Color

echo -e "${GREEN}>>> Начинаю настройку сервера для Flass...${NC}"

# 1. Обновление системы
apt-get update && apt-get upgrade -y

# 2. Установка Docker (официальный скрипт)
echo -e "${GREEN}>>> Установка Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker

# 3. Установка Fail2ban и базовая защита SSH
echo -e "${GREEN}>>> Настройка Fail2ban...${NC}"
apt-get install -y fail2ban
cat <<EOF > /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF
systemctl restart fail2ban

# Создаем структуру проекта (путь на хосте)
echo -e "${GREEN}>>> Создание папок проекта...${NC}"
PROJECT_DIR="/opt/flass"
mkdir -p $PROJECT_DIR/logs
touch $PROJECT_DIR/.env

# Переходим в папку, чтобы последующие команды (если будут) работали там
cd $PROJECT_DIR

# 5. Установка часового пояса (Кыргызстан)
timedatectl set-timezone Asia/Bishkek

echo -e "${GREEN}>>> Настройка завершена!${NC}"
echo "Не забудь заполнить /opt/flass/.env своими API ключами."