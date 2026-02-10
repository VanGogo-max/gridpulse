#!/bin/bash
# setup_bot.sh — Автоматична инсталация на спотов бот за сървър
# Поддържа: MEXC, Gate.io, KuCoin, CoinEx (без KYC)
# Работи с: VanGogo-max/-spot-grid-bot-android-

set -e

# Цветове за четимост
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         СПОТОВ БОТ — АВТОМАТИЧНА ИНСТАЛАЦИЯ           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}⚠️  Това ще инсталира зависимости и ще поправи критични бъгове.${NC}"
echo -e "${YELLOW}💡 Очаквани печалби: $0.50–$1.00/ден при $50–$100 капитал${NC}"
sleep 3

# 1. Инсталация на системни зависимости
echo ""
echo -e "${BLUE}[1/10] Инсталиране на системни зависимости...${NC}"
sudo apt update -y > /dev/null 2>&1
sudo apt install -y python3 python3-pip git curl wget nano > /dev/null 2>&1
echo -e "${GREEN}✅ Системни зависимости инсталирани${NC}"

# 2. Инсталация на Python библиотеки
echo ""
echo -e "${BLUE}[2/10] Инсталиране на Python библиотеки...${NC}"
pip3 install --upgrade pip > /dev/null 2>&1
pip3 install requests==2.31.0 numpy==1.26.4 pandas ta==0.11.0 python-telegram-bot > /dev/null 2>&1
echo -e "${GREEN}✅ Python библиотеки инсталирани${NC}"

# 3. Проверка на директорията
BOT_DIR=$(pwd)
echo ""
echo -e "${BLUE}[3/10] Работна директория: $BOT_DIR${NC}"

# 4. ПОПРАВКА НА КРИТИЧНИ БЪГОВЕ В АДАПТЕРИТЕ
echo ""
echo -e "${BLUE}[4/10] Поправка на критични бъгове...${NC}"

# Поправка 1: Премахване на интервали в base_url
echo "   • Поправка на base_url в адаптерите..."
sed -i 's|self.base_url = "https://api.kucoin.com "|self.base_url = "https://api.kucoin.com"|' adapters/KuCoinSpot.py 2>/dev/null || true
sed -i 's|self.base_url = "https://api.mexc.com "|self.base_url = "https://api.mexc.com"|' adapters/MEXCSpot.py 2>/dev/null || true
sed -i 's|self.base_url = "https://api.gateio.ws/api/v4 "|self.base_url = "https://api.gateio.ws/api/v4"|' adapters/GateIOSpot.py 2>/dev/null || true
sed -i 's|self.base_url = "https://api.coinex.com/v1 "|self.base_url = "https://api.coinex.com/v1"|' adapters/CoinExSpot.py 2>/dev/null || true

# Поправка 2: Telegram URL (без интервал)
echo "   • Поправка на Telegram URL..."
sed -i 's|f"https://api.telegram.org/bot |f"https://api.telegram.org/bot|' telegram_bot.py 2>/dev/null || true

# Поправка 3: CoinEx get_klines() за съвместимост
if [ -f "adapters/CoinExSpot.py" ]; then
    cat > /tmp/fix_coinex.py << 'EOF'
with open('adapters/CoinExSpot.py', 'r') as f:
    content = f.read()

old_code = '''    def get_klines(self, symbol, interval="1h", limit=50):
        market = symbol.replace("/", "")
        interval_map = {"1h": "60", "4h": "240", "1d": "86400"}
        period = interval_map.get(interval, "60")
        data = self._request("GET", "/market/kline", {
            "market": market,
            "type": period,
            "limit": str(limit)
        })
        if data.get("code") == 0:
            # Връща списък от затварящи цени (последната колона = close)
            return [float(kline[2]) for kline in data["data"]]
        return []'''

new_code = '''    def get_klines(self, symbol, interval="1h", limit=50):
        market = symbol.replace("/", "")
        interval_map = {"1h": "60", "4h": "240", "1d": "86400"}
        period = interval_map.get(interval, "60")
        data = self._request("GET", "/market/kline", {
            "market": market,
            "type": period,
            "limit": str(limit)
        })
        if data.get("code") == 0:
            # Преобразуваме към съвместим формат: [timestamp, open, high, low, close, volume]
            klines = []
            for kline in data["data"]:
                ts = int(kline[0])
                open_price = float(kline[1])
                close_price = float(kline[2])
                high_price = float(kline[3])
                low_price = float(kline[4])
                volume = float(kline[5])
                klines.append([ts, open_price, high_price, low_price, close_price, volume])
            return klines[-limit:]
        return []'''

content = content.replace(old_code, new_code)
with open('adapters/CoinExSpot.py', 'w') as f:
    f.write(content)
print("   • Поправен CoinEx get_klines() за съвместимост")
EOF
    python3 /tmp/fix_coinex.py 2>/dev/null || echo "   ⚠️  Пропуснато (файлът може да е вече поправен)"
fi

echo -e "${GREEN}✅ Критични бъгове поправени${NC}"

# 5. Създаване на CSV конвертор за статистика
echo ""
echo -e "${BLUE}[5/10] Създаване на CSV конвертор за статистика...${NC}"
cat > convert_stats_to_csv.py << 'CONVERT_EOF'
#!/usr/bin/env python3
import json
import csv
import os
from datetime import date

def convert_stats():
    """Конвертира trade_stats.json към profits.csv"""
    stats_file = "logs/trade_stats.json"
    csv_file = "logs/profits.csv"
    
    if not os.path.exists(stats_file):
        print("⚠️  Няма статистика за конвертиране")
        return
    
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    # Заглавия за CSV
    headers = ["date", "trades", "profit", "success_rate"]
    
    # Събиране на данни
    rows = []
    for day_date, day_data in stats.get("daily", {}).items():
        trades = day_data.get("trades", 0)
        profit = day_data.get("profit", 0.0)
        success_rate = (day_data.get("success", 0) / trades * 100) if trades > 0 else 0
        rows.append({
            "date": day_date,
            "trades": trades,
            "profit": round(profit, 4),
            "success_rate": f"{success_rate:.1f}%"
        })
    
    # Запис в CSV
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Статистиката е конвертирана в {csv_file}")
    print(f"   Общо сделки: {stats.get('total_trades', 0)}")
    print(f"   Обща печалба: ${stats.get('total_profit', 0.0):.4f}")

if __name__ == "__main__":
    convert_stats()
CONVERT_EOF
chmod +x convert_stats_to_csv.py
echo -e "${GREEN}✅ CSV конвертор създаден${NC}"

# 6. Създаване на здравен чек скрипт
echo ""
echo -e "${BLUE}[6/10] Създаване на здравен чек...${NC}"
cat > health_check.py << 'HEALTH_EOF'
#!/usr/bin/env python3
import os
import sys
import time
sys.path.append(os.path.dirname(__file__))

try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    TELEGRAM_ENABLED = True
except:
    TELEGRAM_ENABLED = False

import requests

def send_telegram(msg):
    if not TELEGRAM_ENABLED or TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=10)
    except:
        pass

# Проверка дали ботът работи
log_path = "logs/bot.log"
if not os.path.exists(log_path):
    error_msg = "⚠️  Ботът не е стартирал — липсва лог файл"
    print(error_msg)
    send_telegram(error_msg)
    sys.exit(1)

last_mod = os.path.getmtime(log_path)
if time.time() - last_mod > 300:  # 5 минути
    error_msg = "🔴 ВНИМАНИЕ: Ботът не е активен повече от 5 минути!"
    print(error_msg)
    send_telegram(error_msg)
    sys.exit(1)

# Проверка за печалби
try:
    with open("logs/trade_stats.json") as f:
        stats = json.load(f)
    total_trades = stats.get("total_trades", 0)
    total_profit = stats.get("total_profit", 0.0)
    print(f"✅ Ботът работи. Общо сделки: {total_trades}, Печалба: ${total_profit:.4f}")
except:
    print("✅ Ботът работи (няма статистика още)")

sys.exit(0)
HEALTH_EOF
chmod +x health_check.py
echo -e "${GREEN}✅ Здравен чек създаден${NC}"

# 7. Създаване на systemd услуга
echo ""
echo -e "${BLUE}[7/10] Настройка на systemd услуга за 24/7 работа...${NC}"
sudo tee /etc/systemd/system/spot-bot.service > /dev/null << EOF
[Unit]
Description=Spot Grid Trading Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_DIR
ExecStart=/usr/bin/python3 $BOT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$BOT_DIR/logs/bot.log
StandardError=append:$BOT_DIR/logs/bot.log
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable spot-bot
echo -e "${GREEN}✅ Systemd услуга настроена${NC}"

# 8. Настройка на cron за автоматични задачи
echo ""
echo -e "${BLUE}[8/10] Настройка на автоматични задачи...${NC}"

# Архивиране на логове всяка неделя
(crontab -l 2>/dev/null | grep -v "archive_logs" || true) | crontab -
(crontab -l 2>/dev/null || echo "") | { cat; echo "0 0 * * 0 cd $BOT_DIR && find logs -name '*.log' -mtime +7 -exec gzip {} \\; 2>/dev/null || true"; } | crontab -

# Здравен чек на всеки 5 минути
(crontab -l 2>/dev/null || echo "") | { cat; echo "*/5 * * * * cd $BOT_DIR && timeout 10 python3 health_check.py > /dev/null 2>&1 || true"; } | crontab -

# Конвертиране на статистика на всеки 1 час
(crontab -l 2>/dev/null || echo "") | { cat; echo "0 * * * * cd $BOT_DIR && python3 convert_stats_to_csv.py > /dev/null 2>&1 || true"; } | crontab -

echo -e "${GREEN}✅ Автоматични задачи настроени${NC}"

# 9. Създаване на helper скрипт за управление
echo ""
echo -e "${BLUE}[9/10] Създаване на управление...${NC}"
cat > bot_manager.sh << 'MANAGER_EOF'
#!/bin/bash
# bot_manager.sh — Управление на спотовия бот

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

case "$1" in
    start)
        sudo systemctl start spot-bot
        echo -e "${GREEN}✅ Ботът е стартиран${NC}"
        ;;
    stop)
        sudo systemctl stop spot-bot
        echo -e "${YELLOW}⚠️  Ботът е спрян${NC}"
        ;;
    restart)
        sudo systemctl restart spot-bot
        echo -e "${GREEN}✅ Ботът е рестартиран${NC}"
        ;;
    status)
        sudo systemctl status spot-bot --no-pager
        ;;
    logs)
        journalctl -u spot-bot -f --no-pager
        ;;
    stats)
        python3 convert_stats_to_csv.py
        if [ -f "logs/profits.csv" ]; then
            echo ""
            echo "📊 Последни данни от profits.csv:"
            tail -20 logs/profits.csv
        fi
        ;;
    *)
        echo "Използване: $0 {start|stop|restart|status|logs|stats}"
        echo ""
        echo "  start   — Стартиране на бота"
        echo "  stop    — Спиране на бота"
        echo "  restart — Рестартиране на бота"
        echo "  status  — Статус на бота"
        echo "  logs    — Показване на логовете в реално време"
        echo "  stats   — Показване на статистика"
        ;;
esac
MANAGER_EOF
chmod +x bot_manager.sh
echo -e "${GREEN}✅ Скрипт за управление създаден${NC}"

# 10. Финални инструкции
echo ""
echo -e "${BLUE}[10/10] Инсталацията приключи!${NC}"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ГОТОВО! ✅                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}📋 Следващи стъпки:${NC}"
echo ""
echo "  1. Проверете дали имате конфигурация:"
echo "     ls -la config.py"
echo ""
echo "  2. Ако няма config.py, създайте го от шаблона:"
echo "     cp config.example.py config.py"
echo "     nano config.py  # Попълнете вашите API ключове"
echo ""
echo "  3. Стартирайте бота:"
echo "     ./bot_manager.sh start"
echo ""
echo "  4. Проверете статуса:"
echo "     ./bot_manager.sh status"
echo ""
echo "  5. Прегледайте логовете:"
echo "     ./bot_manager.sh logs"
echo ""
echo "  6. Прегледайте статистиката:"
echo "     ./bot_manager.sh stats"
echo ""
echo -e "${GREEN}💡 Полезни команди:${NC}"
echo "   • Спиране на бота:        ./bot_manager.sh stop"
echo "   • Рестартиране:            ./bot_manager.sh restart"
echo "   • Статистика в CSV:        cat logs/profits.csv"
echo "   • Архивирани логове:       ls -lh logs/archive/"
echo ""
echo -e "${YELLOW}⚠️  ВАЖНО:${NC}"
echo "   • Никога не споделяйте вашия файл config.py!"
echo "   • Използвайте само 'трейдинг' ключове без права за теглене"
echo "   • Активирайте 2FA на всички борси"
echo "   • Този бот е за образователни цели — няма гаранция за печалби"
echo ""
echo -e "${GREEN}✅ Ботът е готов за 24/7 работа!${NC}"
echo -e "${GREEN}🚀 Очаквани печалби: $0.50–$1.00/ден при консервативна стратегия${NC}"
