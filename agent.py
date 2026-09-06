import json
import urllib.request


COINBASE_API = "https://api.exchange.coinbase.com/products"

SUPPORTED_SYMBOLS = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
}


def get_price(symbol):
    symbol = symbol.upper().replace("/", "")

    if symbol not in SUPPORTED_SYMBOLS:
        return {"error": f"Unsupported symbol: {symbol}"}

    product = SUPPORTED_SYMBOLS[symbol]
    url = f"{COINBASE_API}/{product}/stats"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Binance-Price-Agent/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        last_price = float(data["last"])
        open_price = float(data["open"])

        change_24h = ((last_price - open_price) / open_price) * 100

        return {
            "symbol": symbol,
            "price": last_price,
            "change_24h": change_24h,
            "high_24h": float(data["high"]),
            "low_24h": float(data["low"]),
            "volume_24h": float(data["volume"]),
        }

    except Exception as error:
        return {"error": str(error)}


def main():
    print("Binance Price Agent")
    print("Read-only market data agent")
    print("Supported symbols: BTCUSDT, ETHUSDT")
    print("Type 'exit' to quit.\n")

    while True:
        symbol = input("Ask for a price: ").strip()

        if symbol.lower() == "exit":
            print("Goodbye!")
            break

        result = get_price(symbol)

        if "error" in result:
            print(f"Error: {result['error']}\n")
            continue

        print("\nMarket Data")
        print(f"Symbol: {result['symbol']}")
        print(f"Price: ${result['price']:,.2f}")
        print(f"24h Change: {result['change_24h']:+.2f}%")
        print(f"24h High: ${result['high_24h']:,.2f}")
        print(f"24h Low: ${result['low_24h']:,.2f}")
        print(f"24h Volume: {result['volume_24h']:,.2f}")
        print()


if __name__ == "__main__":
    main()
