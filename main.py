from datetime import datetime

from flask import Flask, request, jsonify
import jsonschema
import json
from jsonschema import validate, ValidationError
import os

from transform import transform_record
from load import load_to_bigquery

port = int(os.environ.get("PORT", 8080))
app = Flask(__name__)

# Load schema from file
with open("schema.json") as f:
    schema = json.load(f)


@app.route("/ingest", methods=["POST"])
def ingest():
    try:
        data = request.get_json()
        schema = {
            "type": "object",
            "properties": {
                "transaction_id": {"type": "string"},
                "amount": {"type": "number"},
                "customer_id": {"type": "string"},
                "product_id": {"type": "string"}

            },
            "required": ["transaction_id", "amount"]
        }
        validate(instance=data, schema=schema)

        #jsonschema.validate(instance=data, schema=schema)

        # Transform data
        tax = round(data["amount"] * 0.18, 2)
        total = round(data["amount"] + tax, 2)
        timestamp = datetime.utcnow().isoformat()


        transformed = {
            "transaction_id": data["transaction_id"],
            "amount": data["amount"],
            "tax": tax,
            "total": total,
            "timestamp":  {
                "type": "string",
                "format": "date-time"
                },
            "customer_id": data["customer_id"],
            "product_id": data["product_id"]
        }
        #transformed = transform_record(data)



        # Step 3: Load to BigQuery
        table_id = "psychic-raceway-461010-a1.http_etl_trigger.transaction_table"
        load_to_bigquery(transformed, table_id)

        # (Later) Load to BigQuery here
        return jsonify({"message": "Success", "data": transformed}), 200

    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": "Invalid data", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

