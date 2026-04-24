from py_eeive import monitor

@monitor(retries=5, retry_delay=1, language="english")
def calculate_logic():
    print("🤖 Начинаю вычисления...")
    result = 10 / 0
    return result

if __name__ == "__main__":
    try:
        calculate_logic()
    except Exception:
        pass