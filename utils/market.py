import ccxt.async_support as ccxt

exchange = ccxt.mexc({'options': {'defaultType': 'swap'}})

async def mexc_check(symbol: str):
    try:
        markets = await exchange.load_markets()
        return f"{symbol}/USDT:USDT" in markets
    except Exception as e:
        print(f"Помилка при перевірці символу на Мексі {symbol}: {e}")
        return False
    finally:
        await exchange.close()  # Закривати після завершення