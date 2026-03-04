"""
Конфигурация на платформата GridPulse
⚠️ Този файл НЕ се качва в GitHub (.gitignore го защитава)
"""

# ========================================
# 💰 ПОРТФЕЙЛ ЗА ПЛАЩАНИЯ
# ========================================

# Твоят адрес за получаване на месечни такси
OWNER_WALLET = "0xfee37e7e64d70f37f96c42375131abb57c1481c2"  # ЗАМЕНИ С ТВОЯ АДРЕС!

# ========================================
# 💳 ЦЕНИ И ТАКСИ
# ========================================

# Месечна такса за реален режим
MONTHLY_FEE_USDT = 15.0

# Реферална награда (процент от месечната такса)
REFERRAL_PERCENT = 10  # 10% за рефералите

# ========================================
# 📊 ТЪРГОВСКИ НАСТРОЙКИ
# ========================================

# Минимален обем за сделка (в USDT)
MIN_TRADE_USDT = 5.0

# Риск на сделка (процент от баланса)
RISK_PERCENT = 0.10  # 10%

# Цел за печалба (процент)
PROFIT_TARGET = 0.003  # 0.3%

# Интервал между проверки (в секунди)
CHECK_INTERVAL = 300  # 5 минути

# ========================================
# 🌐 ТЪРГОВСКИ ДВОЙКИ
# ========================================

# 50+ популярни двойки, налични на всички 4 борси (вероятно)
TRADE_SYMBOLS = [
    # ===== Основни криптовалути =====
    "BTC/USDT",    # Bitcoin
    "ETH/USDT",    # Ethereum
    "BNB/USDT",    # Binance Coin
    "SOL/USDT",    # Solana
    "XRP/USDT",    # Ripple
    "ADA/USDT",    # Cardano
    "DOGE/USDT",   # Dogecoin
    "AVAX/USDT",   # Avalanche
    "MATIC/USDT",  # Polygon
    "LINK/USDT",   # Chainlink
    
    # ===== Layer 1 & Layer 2 =====
    "DOT/USDT",    # Polkadot
    "LTC/USDT",    # Litecoin
    "ATOM/USDT",   # Cosmos
    "UNI/USDT",    # Uniswap
    "ETC/USDT",    # Ethereum Classic
    "FIL/USDT",    # Filecoin
    "NEAR/USDT",   # NEAR Protocol
    "APT/USDT",    # Aptos
    "SUI/USDT",    # Sui
    "ARB/USDT",    # Arbitrum
    "OP/USDT",     # Optimism
    "IMX/USDT",    # Immutable X
    "RNDR/USDT",   # Render Token
    "INJ/USDT",    # Injective
    
    # ===== DeFi токени =====
    "AAVE/USDT",   # Aave
    "MKR/USDT",    # Maker
    "SNX/USDT",    # Synthetix
    "CRV/USDT",    # Curve DAO
    "COMP/USDT",   # Compound
    "YFI/USDT",    # Yearn Finance
    "SUSHI/USDT",  # SushiSwap
    
    # ===== Мем коинове =====
    "PEPE/USDT",   # Pepe
    "SHIB/USDT",   # Shiba Inu
    "FLOKI/USDT",  # Floki
    "BONK/USDT",   # Bonk
    "WIF/USDT",    # dogwifhat
    
    # ===== GameFi & NFT =====
    "SAND/USDT",   # The Sandbox
    "MANA/USDT",   # Decentraland
    "AXS/USDT",    # Axie Infinity
    "GALA/USDT",   # Gala
    "ENJ/USDT",    # Enjin Coin
    
    # ===== Допълнителни популярни =====
    "TRX/USDT",    # TRON
    "XLM/USDT",    # Stellar
    "ALGO/USDT",   # Algorand
    "VET/USDT",    # VeChain
    "ICP/USDT",    # Internet Computer
    "HBAR/USDT",   # Hedera
    "EGLD/USDT",   # MultiversX (Elrond)
    "THETA/USDT",  # Theta Network
    "FTM/USDT",    # Fantom
    "NEO/USDT",    # NEO
    "ZEC/USDT",    # Zcash
    "DASH/USDT",   # Dash
    "XMR/USDT",    # Monero
    "CAKE/USDT",   # PancakeSwap
    "GRT/USDT",    # The Graph
    "CHZ/USDT",    # Chiliz
    "KAVA/USDT",   # Kava
    "ONE/USDT",    # Harmony
    "ROSE/USDT",   # Oasis Network
    "MINA/USDT",   # Mina Protocol
    "ICX/USDT",    # ICON
    "ZIL/USDT",    # Zilliqa
    "BAT/USDT",    # Basic Attention Token
    "1INCH/USDT",  # 1inch
    "LDO/USDT",    # Lido DAO
    "STX/USDT",    # Stacks
    "FLOW/USDT",   # Flow
    "XTZ/USDT",    # Tezos
    "KSM/USDT",    # Kusama
    "CELO/USDT",   # Celo
    "AR/USDT",     # Arweave
    "ENS/USDT",    # Ethereum Name Service
    "MASK/USDT",   # Mask Network
    "AUDIO/USDT",  # Audius
    "ANKR/USDT",   # Ankr
    "SKL/USDT",    # SKALE Network
    "NKN/USDT",    # NKN
    "OGN/USDT",    # Origin Protocol
    "BAND/USDT",   # Band Protocol
    "CTSI/USDT",   # Cartesi
    "SRM/USDT",    # Serum
    "RAY/USDT",    # Raydium
    "LRC/USDT",    # Loopring
    "BAL/USDT",    # Balancer
    "KNC/USDT",    # Kyber Network
    "OCEAN/USDT",  # Ocean Protocol
    "RLC/USDT",    # iExec RLC
    "STORJ/USDT",  # Storj
    "BNT/USDT",    # Bancor
    "REN/USDT",    # Ren
    "QTUM/USDT",   # Qtum
    "WAVES/USDT",  # Waves
    "SC/USDT",     # Siacoin
    "DCR/USDT",    # Decred
    "RVN/USDT",    # Ravencoin
    "KDA/USDT",    # Kadena
    "ELF/USDT",    # aelf
    "CKB/USDT",    # Nervos Network
    "IOTA/USDT",   # IOTA
    "XEM/USDT",    # NEM
    "ONT/USDT",    # Ontology
    "ZRX/USDT",    # 0x
    "REP/USDT",    # Augur
    "KAVA/USDT",   # Kava
    "TOMO/USDT",   # TomoChain
    "WAN/USDT",    # Wanchain
    "BTS/USDT",    # BitShares
    "LSK/USDT",    # Lisk
    "STEEM/USDT",  # Steem
    "SBD/USDT",    # Steem Dollars
    "HIVE/USDT",   # Hive
    "HBD/USDT",    # Hive Dollar
    "EOS/USDT",    # EOS
    "TRX/USDT",    # TRON
    "BTT/USDT",    # BitTorrent
    "WIN/USDT",    # WINkLink
    "JST/USDT",    # JUST
    "SUN/USDT",    # Sun
    "MDX/USDT",    # Mdex
    "BAKE/USDT",   # BakeryToken
    "BURGER/USDT", # Burger Swap
    "CAKE/USDT",   # PancakeSwap
    "VVS/USDT",    # VVS Finance
    "RACA/USDT",   # Radio Caca
    "TLM/USDT",    # Alien Worlds
    "GMT/USDT",    # STEPN
    "GALA/USDT",   # Gala
    "MANA/USDT",   # Decentraland
    "SAND/USDT",   # The Sandbox
    "AXS/USDT",    # Axie Infinity
    "ENJ/USDT",    # Enjin Coin
    "CHZ/USDT",    # Chiliz
    "ALICE/USDT",  # My Neighbor Alice
    "ILV/USDT",    # Illuvium
    "GODS/USDT",   # Gods Unchained
    "MBOX/USDT",   # MOBOX
    "TUS/USDT",    # Treasure Under Sea
    "ATLAS/USDT",  # Star Atlas
    "POLIS/USDT",  # Polis
    "STARL/USDT",  # Starlink
    "NFT/USDT",    # NFT Protocol
    "RFOX/USDT",   # RedFox Labs
    "DEP/USDT",    # DEAPCOIN
    "PLA/USDT",    # PlayDapp
    "HIGH/USDT",   # Highstreet
    "DREAMS/USDT", # Meta Dreams
    "METIS/USDT",  # MetisDAO
    "LOOKS/USDT",  # LooksRare
    "GAL/USDT",    # Galxe
    "FWB/USDT",    # Friends With Benefits
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT......",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "......",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "FWT/USDT",    # Freeway Token
    "......

# ========================================
# 🔗 БЛОКЧЕЙН НАСТРОЙКИ (Polygon)
# ========================================

POLYGON_RPC_URL = "https://polygon-rpc.com"  # Публичен RPC
USDT_CONTRACT = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"  # USDT в Polygon
POLYGONSCAN_API_KEY=V5CHMSVAYDQ9AUDPDN5AQ287EZ6Y5XTQAK
# ========================================
# ⚠️ ВАЖНО
# ========================================

# Този файл съдържа чувствителна информация!
# НИКОГА не го качвай в GitHub!
# .gitignore вече го защитава, но проверявай преди 'git commit'
