import re
from collections import Counter
from typing import List, Dict
from decimal import Decimal
from datetime import datetime

_ACCOUNT_RE = re.compile(r'\b\d{20}\b')

def _clean_account(s: str) -> str:
    if not s:
        return ""
    return re.sub(r'\D', '', s)

def _normalize_counterparty(name: str) -> str:
    return re.sub(r'\s+', ' ', name.strip()) if name else ""

def _parse_date(s: str):
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            continue
    return None

def parse_txt(file_content: str) -> List[Dict]:
    print("=== ПАРСЕР ЗАПУЩЕН ===")
    lines = file_content.splitlines()
    main_accounts = set()

    for line in lines[:1000]:
        if 'РасчСчет' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                acc = _clean_account(parts[1])
                if len(acc) >= 10:
                    main_accounts.add(acc)

    if not main_accounts:
        all_accs = []
        for line in lines[:5000]:
            all_accs.extend(_ACCOUNT_RE.findall(line))
        if all_accs:
            most = Counter(all_accs).most_common(3)
            for acc, _ in most:
                main_accounts.add(_clean_account(acc))

    if not main_accounts:
        print("!!! Не удалось определить основной расчетный счет.")
        return []

    main_accounts = {a for a in main_accounts if a}
    print("Определены основные счета:", main_accounts)

    transactions = []
    in_doc = False
    doc = {}

    payer_keys = {'плательщиксчет', 'плательщикрасчсчет', 'плательщикрасчётныйсчет'}
    receiver_keys = {'получательсчет', 'получательрасчсчет', 'получательрасчётныйсчет'}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if line.startswith('СекцияДокумент='):
            in_doc = True
            doc = {}
            doc['__type'] = line.split('=', 1)[1].strip()
            continue

        if in_doc and line == 'КонецДокумента':
            in_doc = False

            payer_acc = ''
            receiver_acc = ''
            for k, v in doc.items():
                kn = ''.join(filter(str.isalnum, k.lower()))
                if kn in payer_keys:
                    payer_acc = _clean_account(v)
                if kn in receiver_keys:
                    receiver_acc = _clean_account(v)

            is_relevant = False
            tx_type = None
            counterparty = ''
            matched_account = None

            if payer_acc and payer_acc in main_accounts:
                is_relevant = True
                tx_type = 'outgoing'
                counterparty = _normalize_counterparty(doc.get('Получатель', doc.get('Получатель1', '')))
                matched_account = payer_acc
            elif receiver_acc and receiver_acc in main_accounts:
                is_relevant = True
                tx_type = 'incoming'
                counterparty = _normalize_counterparty(doc.get('Плательщик', doc.get('Плательщик1', '')))
                matched_account = receiver_acc
            else:
                for v in doc.values():
                    m = _ACCOUNT_RE.search(str(v))
                    if m and m.group(0) in main_accounts:
                        is_relevant = True
                        tx_type = 'outgoing' if any(k.lower().startswith('плательщик') for k in doc.keys()) else 'incoming'
                        matched_account = m.group(0)
                        counterparty = _normalize_counterparty(doc.get('Получатель', doc.get('Плательщик', '')))
                        break

            if not is_relevant:
                doc = {}
                continue

            amount_raw = doc.get('Сумма', '0').replace(',', '.').strip()
            try:
                amount = float(Decimal(amount_raw))
            except:
                try:
                    amt_m = re.search(r'[-+]?\d+[\.,]?\d*', amount_raw)
                    amount = float(amt_m.group(0).replace(',', '.')) if amt_m else 0.0
                except:
                    amount = 0.0

            if amount <= 0:
                doc = {}
                continue

            tr_date = _parse_date(doc.get('Дата', doc.get('ДатаСписано', doc.get('ДатаПоступило', ''))))
            purpose = doc.get('НазначениеПлатежа', '') or doc.get('Назначение', '')

            transactions.append({
                "date": tr_date,
                "amount": amount,
                "type": tx_type,
                "counterparty": counterparty,
                "purpose": f"{doc.get('__type','')}: {purpose}"[:300],
                "account": matched_account or list(main_accounts)[0]
            })

            doc = {}
            continue

        if in_doc and '=' in line:
            k, v = line.split('=', 1)
            doc[k.strip()] = v.strip()

    print(f"=== ПАРСЕР ЗАВЕРШИЛ: {len(transactions)} транзакций ===")
    return transactions
