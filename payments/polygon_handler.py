"""
Модул за работа с плащания в Polygon мрежата
Проверява транзакции в блокчейна и потвърждава плащания
"""

from web3 import Web3
import requests
from datetime import datetime
import time

# Конфигурация (ще се зарежда от config.py)
POLYGON_RPC_URL = "https://polygon-rpc.com"
USDT_CONTRACT = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"  # USDT в Polygon
OWNER_WALLET = None  # Ще се зареди от конфигурацията
MONTHLY_FEE = 15.0   # $15/месец

# Инициализация на Web3
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

def init_polygon_handler(config):
    """
    Инициализира модула с конфигурация
    
    Args:
        config: Обект с конфигурация (OWNER_WALLET, POLYGON_RPC_URL, и т.н.)
    """
    global OWNER_WALLET, POLYGON_RPC_URL, w3
    
    OWNER_WALLET = config.OWNER_WALLET
    POLYGON_RPC_URL = config.POLYGON_RPC_URL
    MONTHLY_FEE = config.MONTHLY_FEE_USDT
    
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
    
    if w3.is_connected():
        print("✅ Polygon RPC е свързан успешно!")
    else:
        print("❌ Грешка: Не може да се свърже с Polygon!")

def check_transaction(tx_hash):
    """
    Проверява дали транзакцията е валидна
    
    Args:
        tx_hash: Хеш на транзакцията
    
    Returns:
        dict с резултат
    """
    try:
        # Получаване на информация за транзакцията
        tx = w3.eth.get_transaction(tx_hash)
        
        # Проверка дали получателят е твоят портфейл
        to_address = tx['to']
        if to_address.lower() != OWNER_WALLET.lower():
            return {
                'success': False,
                'error': 'Транзакцията не е към правилния адрес'
            }
        
        # Получаване на сумата в USDT
        # USDT е ERC-20 токен, затова трябва да проверим трансфера в смарт контракта
        amount = get_usdt_amount_from_tx(tx_hash)
        
        if amount is None:
            return {
                'success': False,
                'error': 'Не може да се получи сумата от транзакцията'
            }
        
        # Проверка дали сумата е достатъчна
        if amount < MONTHLY_FEE:
            return {
                'success': False,
                'error': f'Сумата е твърде малка. Минимум: ${MONTHLY_FEE}'
            }
        
        # Получаване на времето на транзакцията
        block = w3.eth.get_block(tx['blockNumber'])
        tx_time = datetime.fromtimestamp(block['timestamp'])
        
        return {
            'success': True,
            'tx_hash': tx_hash,
            'amount': amount,
            'to_address': to_address,
            'timestamp': tx_time.isoformat(),
            'block_number': tx['blockNumber']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_usdt_amount_from_tx(tx_hash):
    """
    Извлича сумата в USDT от транзакция към USDT контракт
    
    Args:
        tx_hash: Хеш на транзакцията
    
    Returns:
        float или None
    """
    try:
        # Извикваме PolygonScan API за да получим детайли за транзакцията
        api_url = f"https://api.polygonscan.com/api?module=account&action=tokentx&txhash={tx_hash}&apikey="
        
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data['status'] == '1' and len(data['result']) > 0:
            # Намираме трансфера на USDT
            for tx in data['result']:
                if tx['contractAddress'].lower() == USDT_CONTRACT.lower():
                    # USDT има 6 десетични знака
                    amount = int(tx['value']) / 10**6
                    return amount
        
        return None
        
    except Exception as e:
        print(f"Грешка при получаване на USDT сума: {e}")
        return None

def verify_payment(tx_hash, expected_amount=None):
    """
    Пълна проверка на плащане
    
    Args:
        tx_hash: Хеш на транзакцията
        expected_amount: Очаквана сума (по избор)
    
    Returns:
        dict с резултат
    """
    # Проверка 1: Дали транзакцията съществува
    result = check_transaction(tx_hash)
    
    if not result['success']:
        return result
    
    # Проверка 2: Дали сумата е правилна
    if expected_amount and abs(result['amount'] - expected_amount) > 0.1:
        return {
            'success': False,
            'error': f'Сумата не съвпада. Очаквана: ${expected_amount}, Получена: ${result["amount"]}'
        }
    
    # Проверка 3: Дали транзакцията е достатъчно нова (в последните 24 часа)
    tx_time = datetime.fromisoformat(result['timestamp'])
    if (datetime.now() - tx_time).total_seconds() > 86400:
        return {
            'success': False,
            'error': 'Транзакцията е по-стара от 24 часа'
        }
    
    return {
        'success': True,
        'tx_hash': tx_hash,
        'amount': result['amount'],
        'confirmed': True,
        'message': 'Плащането е потвърдено!'
    }

def monitor_payments(callback_function, check_interval=60):
    """
    Мониторира нови плащания в реално време
    (Този метод се изпълнява в отделен поток)
    
    Args:
        callback_function: Функция, която се извиква при ново плащане
        check_interval: Интервал между проверки (в секунди)
    """
    print(f"🔍 Мониторинг на плащания започна... (проверка на всеки {check_interval} сек)")
    
    while True:
        try:
            # Тук ще се проверяват нови транзакции към твоя портфейл
            # За сега просто чакаме
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("⏹️ Мониторингът е спрян")
            break
        except Exception as e:
            print(f"❌ Грешка при мониторинг: {e}")
            time.sleep(check_interval)

def get_wallet_balance(address=None):
    """
    Връща баланса на портфейл в USDT
    
    Args:
        address: Адрес на портфейл (по подразбиране твоят)
    
    Returns:
        float баланс в USDT
    """
    if address is None:
        address = OWNER_WALLET
    
    try:
        # Използваме PolygonScan API
        api_url = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={USDT_CONTRACT}&address={address}&tag=latest&apikey="
        
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data['status'] == '1':
            balance = int(data['result']) / 10**6  # USDT има 6 десетични знака
            return balance
        
        return 0.0
        
    except Exception as e:
        print(f"Грешка при получаване на баланс: {e}")
        return 0.0

def generate_payment_address(user_id):
    """
    Генерира уникален адрес за плащане за потребител
    (В бъдеще може да се използват подадреси или други методи)
    
    Args:
        user_id: ID на потребител
    
    Returns:
        str адрес за плащане
    """
    # Засега връщаме основния адрес
    # В бъдеще може да се използват подадреси или отделни портфейли
    return OWNER_WALLET

# Тестова функция
if __name__ == '__main__':
    print("🧪 Тестване на Polygon модул...")
    
    # Тестова транзакция (замени с реален хеш)
    test_tx_hash = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    
    result = check_transaction(test_tx_hash)
    
    if result['success']:
        print(f"✅ Транзакцията е валидна!")
        print(f"   Сума: ${result['amount']}")
        print(f"   Време: {result['timestamp']}")
    else:
        print(f"❌ Грешка: {result['error']}")
