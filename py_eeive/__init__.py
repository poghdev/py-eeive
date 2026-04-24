import functools
import time
import traceback
import os
import asyncio
import inspect
import json
import platform
import random
import urllib.request
from urllib.parse import urlparse, parse_qs
from datetime import datetime

ERRORS = {
    "english": {
        "ZeroDivisionError": {
            "cause": "You are dividing a number by zero.",
            "fix":   "Check that the denominator is not 0 before dividing.",
        },
        "FileNotFoundError": {
            "cause": "The file was not found at the specified path.",
            "fix":   "Make sure the file exists and the path is correct.",
        },
        "KeyError": {
            "cause": "The key does not exist in the dictionary.",
            "fix":   "Use .get('key') instead of ['key'], or check if the key exists first.",
        },
        "IndexError": {
            "cause": "You are accessing an index that does not exist in the list.",
            "fix":   "Check the length of the list before accessing an index.",
        },
        "TypeError": {
            "cause": "You are using the wrong data type.",
            "fix":   "Check the types of your variables (e.g. str vs int).",
        },
        "ValueError": {
            "cause": "A variable has an unexpected value.",
            "fix":   "Check the value you are passing to the function.",
        },
        "AttributeError": {
            "cause": "The object does not have this attribute or method.",
            "fix":   "Check for typos in the method name or verify the object type.",
        },
        "ImportError": {
            "cause": "The module could not be imported.",
            "fix":   "Make sure the package is installed: pip install <package_name>.",
        },
        "ModuleNotFoundError": {
            "cause": "The module was not found.",
            "fix":   "Install it with: pip install <module_name>.",
        },
        "NameError": {
            "cause": "You are using a variable that has not been defined.",
            "fix":   "Check that the variable is defined before using it.",
        },
        "RecursionError": {
            "cause": "The function is calling itself too many times.",
            "fix":   "Check your recursion logic and add a proper base case.",
        },
        "MemoryError": {
            "cause": "The program ran out of memory.",
            "fix":   "Try processing data in smaller chunks.",
        },
        "TimeoutError": {
            "cause": "The operation took too long and timed out.",
            "fix":   "Increase the timeout or check your network connection.",
        },
        "ConnectionError": {
            "cause": "Could not connect to the server.",
            "fix":   "Check your internet connection and the server URL.",
        },
        "PermissionError": {
            "cause": "You do not have permission to access this file or folder.",
            "fix":   "Check file permissions or run as administrator.",
        },
        "IsADirectoryError": {
            "cause": "You are trying to open a directory as a file.",
            "fix":   "Make sure the path points to a file, not a folder.",
        },
        "NotADirectoryError": {
            "cause": "The path is not a directory.",
            "fix":   "Check the path you are using.",
        },
        "OSError": {
            "cause": "An OS-level error occurred.",
            "fix":   "Check file paths, permissions, and disk space.",
        },
        "RuntimeError": {
            "cause": "A general runtime error occurred.",
            "fix":   "Read the full error message for more details.",
        },
        "StopIteration": {
            "cause": "The iterator has no more items.",
            "fix":   "Check your loop logic or use a try/except around next().",
        },
        "OverflowError": {
            "cause": "The number is too large for the data type.",
            "fix":   "Use a smaller number or a different data type.",
        },
        "UnicodeDecodeError": {
            "cause": "Could not decode the text — wrong encoding.",
            "fix":   "Try opening the file with encoding='utf-8' or encoding='latin-1'.",
        },
        "UnicodeEncodeError": {
            "cause": "Could not encode the text.",
            "fix":   "Use encode('utf-8', errors='ignore') or check your string.",
        },
        "JSONDecodeError": {
            "cause": "The JSON data is invalid or malformed.",
            "fix":   "Validate your JSON at jsonlint.com or check the source.",
        },
        "SyntaxError": {
            "cause": "There is a syntax error in your code.",
            "fix":   "Check for missing colons, brackets, or quotes.",
        },
        "IndentationError": {
            "cause": "The indentation is incorrect.",
            "fix":   "Make sure you are using consistent spaces or tabs.",
        },
        "AssertionError": {
            "cause": "An assert statement failed.",
            "fix":   "Check the condition in your assert statement.",
        },
        "NotImplementedError": {
            "cause": "This method is not implemented yet.",
            "fix":   "Implement the method or use a different one.",
        },
        "EOFError": {
            "cause": "Reached the end of file unexpectedly.",
            "fix":   "Check that your input source has the expected data.",
        },
        "BrokenPipeError": {
            "cause": "The connection was closed before data was fully sent.",
            "fix":   "Handle the BrokenPipeError with try/except.",
        },
    },
    "russian": {
        "ZeroDivisionError": {
            "cause": "Ты делишь число на ноль.",
            "fix":   "Проверь что знаменатель не равен 0 перед делением.",
        },
        "FileNotFoundError": {
            "cause": "Файл не найден по указанному пути.",
            "fix":   "Убедись что файл существует и путь указан правильно.",
        },
        "KeyError": {
            "cause": "Такого ключа нет в словаре.",
            "fix":   "Используй .get('ключ') вместо ['ключ'], или сначала проверь наличие ключа.",
        },
        "IndexError": {
            "cause": "Обращаешься к индексу которого нет в списке.",
            "fix":   "Проверь длину списка перед обращением к индексу.",
        },
        "TypeError": {
            "cause": "Используется неправильный тип данных.",
            "fix":   "Проверь типы переменных (например str вместо int).",
        },
        "ValueError": {
            "cause": "Переменная имеет неожиданное значение.",
            "fix":   "Проверь значение которое передаёшь в функцию.",
        },
        "AttributeError": {
            "cause": "У объекта нет такого атрибута или метода.",
            "fix":   "Проверь опечатки в названии метода или тип объекта.",
        },
        "ImportError": {
            "cause": "Модуль не удалось импортировать.",
            "fix":   "Убедись что пакет установлен: pip install <название_пакета>.",
        },
        "ModuleNotFoundError": {
            "cause": "Модуль не найден.",
            "fix":   "Установи его командой: pip install <название_модуля>.",
        },
        "NameError": {
            "cause": "Используется переменная которая не была объявлена.",
            "fix":   "Убедись что переменная определена до её использования.",
        },
        "RecursionError": {
            "cause": "Функция вызывает себя слишком много раз.",
            "fix":   "Проверь логику рекурсии и добавь условие выхода.",
        },
        "MemoryError": {
            "cause": "Программе не хватило памяти.",
            "fix":   "Попробуй обрабатывать данные меньшими частями.",
        },
        "TimeoutError": {
            "cause": "Операция заняла слишком много времени.",
            "fix":   "Увеличь таймаут или проверь подключение к сети.",
        },
        "ConnectionError": {
            "cause": "Не удалось подключиться к серверу.",
            "fix":   "Проверь интернет-соединение и URL сервера.",
        },
        "PermissionError": {
            "cause": "Нет прав доступа к файлу или папке.",
            "fix":   "Проверь права доступа или запусти от имени администратора.",
        },
        "IsADirectoryError": {
            "cause": "Ты пытаешься открыть папку как файл.",
            "fix":   "Убедись что путь указывает на файл, а не на папку.",
        },
        "NotADirectoryError": {
            "cause": "Это не директория.",
            "fix":   "Проверь путь который используешь.",
        },
        "OSError": {
            "cause": "Произошла ошибка на уровне операционной системы.",
            "fix":   "Проверь пути к файлам, права доступа и свободное место на диске.",
        },
        "RuntimeError": {
            "cause": "Произошла общая ошибка во время выполнения.",
            "fix":   "Прочитай полное сообщение об ошибке для деталей.",
        },
        "StopIteration": {
            "cause": "В итераторе больше нет элементов.",
            "fix":   "Проверь логику цикла или используй try/except вокруг next().",
        },
        "OverflowError": {
            "cause": "Число слишком большое для данного типа данных.",
            "fix":   "Используй меньшее число или другой тип данных.",
        },
        "UnicodeDecodeError": {
            "cause": "Не удалось декодировать текст — неправильная кодировка.",
            "fix":   "Попробуй открыть файл с encoding='utf-8' или encoding='latin-1'.",
        },
        "UnicodeEncodeError": {
            "cause": "Не удалось закодировать текст.",
            "fix":   "Используй encode('utf-8', errors='ignore') или проверь строку.",
        },
        "JSONDecodeError": {
            "cause": "JSON данные некорректны или повреждены.",
            "fix":   "Проверь JSON на jsonlint.com или проверь источник данных.",
        },
        "SyntaxError": {
            "cause": "В коде есть синтаксическая ошибка.",
            "fix":   "Проверь пропущенные двоеточия, скобки или кавычки.",
        },
        "IndentationError": {
            "cause": "Неправильные отступы в коде.",
            "fix":   "Убедись что используешь одинаковые пробелы или табы.",
        },
        "AssertionError": {
            "cause": "Не выполнилось условие assert.",
            "fix":   "Проверь условие в своём операторе assert.",
        },
        "NotImplementedError": {
            "cause": "Этот метод ещё не реализован.",
            "fix":   "Реализуй метод или используй другой.",
        },
        "EOFError": {
            "cause": "Неожиданно достигнут конец файла.",
            "fix":   "Проверь что источник данных содержит ожидаемые данные.",
        },
        "BrokenPipeError": {
            "cause": "Соединение было закрыто до завершения передачи данных.",
            "fix":   "Обработай BrokenPipeError через try/except.",
        },
    },
    "spanish": {
        "ZeroDivisionError": {
            "cause": "Estás dividiendo un número por cero.",
            "fix":   "Verifica que el denominador no sea 0 antes de dividir.",
        },
        "FileNotFoundError": {
            "cause": "No se encontró el archivo en la ruta especificada.",
            "fix":   "Asegúrate de que el archivo exista y la ruta sea correcta.",
        },
        "KeyError": {
            "cause": "La clave no existe en el diccionario.",
            "fix":   "Usa .get('key') o verifica si la clave existe primero.",
        },
        "IndexError": {
            "cause": "Acceso a un índice que no existe en la lista.",
            "fix":   "Verifica la longitud de la lista antes de acceder.",
        },
        "TypeError": {
            "cause": "Tipo de dato incorrecto.",
            "fix":   "Revisa los tipos de tus variables (ej. str vs int).",
        },
        "ValueError": {
            "cause": "Valor inesperado en una variable.",
            "fix":   "Revisa el valor que pasas a la función.",
        },
        "AttributeError": {
            "cause": "El objeto no tiene este atributo o método.",
            "fix":   "Revisa errores tipográficos o el tipo de objeto.",
        },
        "NameError": {
            "cause": "Variable no definida.",
            "fix":   "Define la variable antes de usarla.",
        },
        "TimeoutError": {
            "cause": "La operación tardó demasiado.",
            "fix":   "Aumenta el tiempo de espera o revisa la red.",
        },
        "PermissionError": {
            "cause": "Sin permisos para acceder al archivo o carpeta.",
            "fix":   "Revisa permisos o ejecuta como administrador.",
        },
    },
    "greek": {
        "ZeroDivisionError": {
            "cause": "Γίνεται διαίρεση με το μηδέν.",
            "fix":   "Ελέγξτε αν ο παρονομαστής είναι 0 πριν τη διαίρεση.",
        },
        "FileNotFoundError": {
            "cause": "Το αρχείο δεν βρέθηκε στην καθορισμένη διαδρομή.",
            "fix":   "Βεβαιωθείτε ότι το αρχείο υπάρχει και η διαδρομή είναι σωστή.",
        },
        "KeyError": {
            "cause": "Το κλειδί δεν υπάρχει στο λεξικό.",
            "fix":   "Χρησιμοποιήστε .get('key') ή ελέγξτε αν το κλειδί υπάρχει.",
        },
        "IndexError": {
            "cause": "Πρόσβαση σε δείκτη που δεν υπάρχει στη λίστα.",
            "fix":   "Ελέγξτε το μήκος της λίστας πριν την πρόσβαση.",
        },
        "TypeError": {
            "cause": "Λανθασμένος τύπος δεδομένων.",
            "fix":   "Ελέγξτε τους τύπους των μεταβλητών σας (π.χ. str vs int).",
        },
        "ValueError": {
            "cause": "Μη αναμενόμενη τιμή σε μια μεταβλητή.",
            "fix":   "Ελέγξτε την τιμή που περνάτε στη συνάρτηση.",
        },
        "AttributeError": {
            "cause": "Το αντικείμενο δεν έχει αυτό το χαρακτηριστικό.",
            "fix":   "Ελέγξτε για τυπογραφικά λάθη ή τον τύπο του αντικειμένου.",
        },
        "NameError": {
            "cause": "Η μεταβλητή δεν έχει οριστεί.",
            "fix":   "Ορίστε τη μεταβλητή πριν τη χρησιμοποιήσετε.",
        },
        "TimeoutError": {
            "cause": "Η λειτουργία άργησε πολύ.",
            "fix":   "Αυξήστε το χρόνο αναμονής ή ελέγξτε το δίκτυο.",
        },
        "PermissionError": {
            "cause": "Δεν έχετε δικαίωμα πρόσβασης στο αρχείο ή το φάκελο.",
            "fix":   "Ελέγξτε τα δικαιώματα ή εκτελέστε ως διαχειριστής.",
        },
    },
}

TEXTS = {
    "english": {
        "starting":    "Starting",
        "success":     "Finished in",
        "seconds":     "sec",
        "attempt":     "Attempt",
        "retrying":    "Retrying in",
        "fatal":       "Script failed permanently",
        "error_type":  "Error",
        "error_line":  "Line",
        "cause":       "Cause",
        "fix":         "Fix",
        "log_saved":   "Log saved",
        "unknown":     "Unknown error — check the traceback above.",
        "in_file":     "in file",
    },
    "russian": {
        "starting":    "Запуск",
        "success":     "Завершён за",
        "seconds":     "сек",
        "attempt":     "Попытка",
        "retrying":    "Повтор через",
        "fatal":       "Скрипт упал окончательно",
        "error_type":  "Ошибка",
        "error_line":  "Строка",
        "cause":       "Причина",
        "fix":         "Решение",
        "log_saved":   "Лог сохранён",
        "unknown":     "Неизвестная ошибка — смотри traceback выше.",
        "in_file":     "в файле",
    },
    "spanish": {
        "starting":    "Iniciando",
        "success":     "Finalizado en",
        "seconds":     "seg",
        "attempt":     "Intento",
        "retrying":    "Reintentando en",
        "fatal":       "El script falló permanentemente",
        "error_type":  "Error",
        "error_line":  "Línea",
        "cause":       "Causa",
        "fix":         "Solución",
        "log_saved":   "Log guardado",
        "unknown":     "Error desconocido — revisa el traceback arriba.",
        "in_file":     "en el archivo",
    },
    "greek": {
        "starting":    "Εκκίνηση",
        "success":     "Ολοκληρώθηκε σε",
        "seconds":     "δευτ",
        "attempt":     "Προσπάθεια",
        "retrying":    "Επανάληψη σε",
        "fatal":       "Η εκτέλεση απέτυχε οριστικά",
        "error_type":  "Σφάλμα",
        "error_line":  "Γραμμή",
        "cause":       "Αιτία",
        "fix":         "Διόρθωση",
        "log_saved":   "Το αρχείο καταγραφής αποθηκεύτηκε",
        "unknown":     "Άγνωστο σφάλμα — ελέγξτε το traceback παραπάνω.",
        "in_file":     "στο αρχείο",
    },
}

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

def _line(char="─", width=50):
    return char * width

def _get_ram_usage():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
    except ImportError:
        return "N/A"

def _filter_locals(locals_data):
    return {k: str(v)[:50] for k, v in locals_data.items() if not k.startswith('__')}

def _get_timing_bar(elapsed, max_elapsed, width=10):
    percent = min(elapsed / max_elapsed, 1.0) if max_elapsed > 0 else 0
    filled = int(percent * width)
    return "█" * filled + "░" * (width - filled)

def _get_error_info(exc, lang, custom_errors=None):
    error_name = type(exc).__name__
    tb = traceback.extract_tb(exc.__traceback__)
    last = tb[-1] if tb else None
    line_no = last.lineno if last else "?"
    filename = os.path.basename(last.filename) if last else "?"
    
    explanation = None
    if custom_errors and error_name in custom_errors:
        explanation = custom_errors[error_name]
    else:
        explanation = ERRORS.get(lang, ERRORS["english"]).get(error_name)
    return error_name, line_no, filename, explanation

def _send_webhook(url, message):
    try:
        payload = {"content": message, "text": message}
        
        if "api.telegram.org" in url:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            chat_id = query_params.get('chat_id', [None])[0]
            if chat_id:
                payload["chat_id"] = chat_id

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            pass
    except:
        pass

def _save_log(func_name, error_name, tb_str, lang, attempts_data=None):
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(log_dir, f"{func_name}_{date_str}.json")
    
    log_data = {
        "timestamp": now.isoformat(),
        "function": func_name,
        "error": error_name,
        "traceback": tb_str,
        "language": lang,
        "attempts": attempts_data,
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "machine": platform.machine()
        }
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4)
    return path

def monitor(retries=1, retry_delay=5, log=True, language="english", custom_errors=None, 
            exponential_backoff=False, retry_on=(Exception,), webhook_url=None, jitter=True):
    retries = max(1, int(retries))
    lang = language.lower()
    if lang not in TEXTS:
        lang = "english"
    t = TEXTS[lang]

    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)

        def handle_failure(attempt, exc, start_time, attempts_data):
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)
            error_name, line_no, filename, explanation = _get_error_info(exc, lang, custom_errors)
            ram = _get_ram_usage()
            
            tb = exc.__traceback__
            while tb.tb_next: tb = tb.tb_next
            filtered_vars = _filter_locals(tb.tb_frame.f_locals)

            attempts_data.append({
                "attempt": attempt,
                "elapsed": elapsed,
                "error": error_name,
                "variables": filtered_vars,
                "ram_usage": ram
            })

            max_elapsed = max([a['elapsed'] for a in attempts_data]) if attempts_data else elapsed
            bar = _get_timing_bar(elapsed, max_elapsed)

            print(
                f"{RED}[py-eeive]{RESET} ❌ "
                f"{t['attempt']} {BOLD}{attempt}/{retries}{RESET} [{bar}] {elapsed}s — RAM: {ram} — "
                f"{t['error_line']} {line_no} — {RED}{error_name}{RESET}"
            )
            
            if filtered_vars:
                var_str = ", ".join([f"{k}={v}" for k, v in filtered_vars.items()])
                print(f"    {DIM}Snapshot: {var_str}{RESET}")
            
            should_retry = attempt < retries and isinstance(exc, retry_on)
            
            base_delay = retry_delay * (2 ** (attempt - 1)) if exponential_backoff else retry_delay
            if jitter and should_retry:
                base_delay *= (0.5 + random.random())
            current_delay = round(base_delay, 2)
            
            if should_retry:
                print(f"{YELLOW}[py-eeive]{RESET} 🔄 {t['retrying']} {current_delay} {t['seconds']}...")
                return True, current_delay
            return False, 0

        def finalize_error(exc, start_time, attempts_data):
            elapsed = round(time.time() - start_time, 2)
            error_name, line_no, filename, explanation = _get_error_info(exc, lang, custom_errors)
            tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

            print(f"\n{RED}{BOLD}" + _line("━") + RESET)
            print(f"{RED}{BOLD}💥 {t['fatal']}{RESET}")
            print(f"{RED}{BOLD}" + _line("━") + RESET)
            print(f"  {BOLD}{t['error_type']}:{RESET}   {RED}{error_name}{RESET}: {exc}")
            print(f"  {BOLD}{t['error_line']}:{RESET}    {line_no} {t['in_file']} {filename}")

            if explanation:
                print(f"  {BOLD}{t['cause']}:{RESET}   {explanation['cause']}")
                print(f"  {BOLD}{t['fix']}:{RESET}  {GREEN}{explanation['fix']}{RESET}")
            else:
                print(f"  {DIM}{t['unknown']}{RESET}")
                for line in tb_str.strip().split('\n'):
                    print(f"  {DIM}{line}{RESET}")

            print(f"{RED}{BOLD}" + _line("━") + RESET)
            print(f"  ⏱  {elapsed} {t['seconds']}")

            if log:
                log_path = _save_log(func.__name__, error_name, tb_str, lang, attempts_data)
                print(f"  📄 {t['log_saved']}: {DIM}{log_path}{RESET}")
            
            if webhook_url:
                msg = f"💥 [py-eeive] {func.__name__} failed: {error_name} at line {line_no}"
                _send_webhook(webhook_url, msg)

            print(f"{RED}{BOLD}" + _line("━") + RESET + "\n")

        if is_async:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                print(f"\n{CYAN}{BOLD}[py-eeive]{RESET} {t['starting']}: {BOLD}{func.__name__}{RESET}")
                print(DIM + _line() + RESET)
                start_time = time.time()
                last_exc = None
                attempts_data = []

                for attempt in range(1, retries + 1):
                    attempt_start = time.time()
                    try:
                        result = await func(*args, **kwargs)
                        elapsed = round(time.time() - start_time, 2)
                        print(f"{GREEN}{BOLD}[py-eeive]{RESET} {GREEN}✅ {t['success']} {BOLD}{elapsed}{RESET} {GREEN}{t['seconds']}{RESET}\n")
                        return result
                    except Exception as exc:
                        last_exc = exc
                        can_retry, delay = handle_failure(attempt, exc, attempt_start, attempts_data)
                        if can_retry:
                            await asyncio.sleep(delay)
                        else:
                            break
                finalize_error(last_exc, start_time, attempts_data)
                raise last_exc
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"\n{CYAN}{BOLD}[py-eeive]{RESET} {t['starting']}: {BOLD}{func.__name__}{RESET}")
                print(DIM + _line() + RESET)
                start_time = time.time()
                last_exc = None
                attempts_data = []

                for attempt in range(1, retries + 1):
                    attempt_start = time.time()
                    try:
                        result = func(*args, **kwargs)
                        elapsed = round(time.time() - start_time, 2)
                        print(f"{GREEN}{BOLD}[py-eeive]{RESET} {GREEN}✅ {t['success']} {BOLD}{elapsed}{RESET} {GREEN}{t['seconds']}{RESET}\n")
                        return result
                    except Exception as exc:
                        last_exc = exc
                        can_retry, delay = handle_failure(attempt, exc, attempt_start, attempts_data)
                        if can_retry:
                            time.sleep(delay)
                        else:
                            break
                finalize_error(last_exc, start_time, attempts_data)
                raise last_exc

        return wrapper
    return decorator