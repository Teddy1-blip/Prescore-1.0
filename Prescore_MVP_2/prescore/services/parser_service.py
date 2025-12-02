# prescore/services/parser_service.py

def parse_file(content: bytes, filename: str):
    """
    Универсальный парсер для FastAPI версии
    """
    print(f"=== PARSER SERVICE: обработка {filename} ===")

    # Для TXT файлов используем тот же парсер что и в Flask
    if filename.endswith(".txt"):
        from prescore.parser.txt_parser import parse_txt
        text_content = content.decode("utf-8", errors="ignore")
        return parse_txt(text_content)

    # Для CSV можно добавить позже
    elif filename.endswith(".csv"):
        # Заглушка для CSV
        return []

    else:
        return []