import json
import urllib.parse
import urllib.request


BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"


def get_price(symbol):
    """Get current Binance price and 24h statistics."""
    symbol = symbol.upper().replace("/", "")

    params = urllib.parse.urlencode({"symbol": symbol})
    url = f"{BINANCE_API}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

        return {
            "symbol": data["symbol"],
            "price": data["lastPrice"],
            "change_24h": data["priceChangePercent"],
            "high_24h": data["highPrice"],
            "low_24h": data["lowPrice"],
            "volume_24h": data["volume"],
        }

    except Exception as error:
        return {"error": str(error)}


def main():
    print("🤖 Binance Price Agent")
    print("Type a symbol such as BTCUSDT, ETHUSDT or BNBUSDT.")
    print("Type 'exit' to quit.\n")

    while True:
        symbol = input("Ask for a price: ").strip()

        if symbol.lower() == "exit":
            print("Goodbye!")
            break

        result = get_price(symbol)

        if "error" in result:
            print(f"❌ Error: {result['error']}\n")
            continue

        print("\n📊 Binance Market Data")
        print(f"Symbol: {result['symbol']}")
        print(f"Price: {result['price']}")
        print(f"24h Change: {result['change_24h']}%")
        print(f"24h High: {result['high_24h']}")
        print(f"24h Low: {result['low_24h']}")
        print(f"24h Volume: {result['volume_24h']}")
        print()


if __name__ == "__main__":
    main()
