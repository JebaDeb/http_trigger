from google.cloud import bigquery

def load_to_bigquery(data, table_id):
    client = bigquery.Client()

    # Convert dict to row format
    rows_to_insert = [data]

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("✅ New rows have been added.")
        return True
    else:
        print("❌ Errors:", errors)
        return False
