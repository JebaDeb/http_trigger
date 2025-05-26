from datetime import datetime

def transform_record(record):
    tax_rate = 0.1  # 10% tax
    record['tax'] = round(record['amount'] * tax_rate, 2)
    record['timestamp'] = datetime.utcnow().isoformat()
    return record
