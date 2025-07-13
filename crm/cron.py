import 
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
import requests

def update_low_stock():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    mutation = '''
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        success
      }
    }
    '''

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            timeout=10
        )
        data = response.json()
        updated_products = data["data"]["updateLowStockProducts"]["updatedProducts"]

        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"\n[{now}] Low-stock restock triggered\n")
            for product in updated_products:
                log.write(f"- {product['name']}: new stock = {product['stock']}\n")

        print("Low-stock products updated.")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log:
            log.write(f"\n[{now}] ERROR: {e}\n")

