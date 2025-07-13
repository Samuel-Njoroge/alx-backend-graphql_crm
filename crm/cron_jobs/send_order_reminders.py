#!/usr/bin/env python3

import datetime
import logging
import sys
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Set up logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Define GraphQL query
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()

query = gql("""
    query GetPendingOrders($fromDate: Date!) {
        orders(orderDate_Gte: $fromDate) {
            id
            customer {
                email
            }
        }
    }
""")

variables = {
    "fromDate": seven_days_ago
}

# Configure GraphQL client
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Execute query and log results
try:
    response = client.execute(query, variable_values=variables)
    orders = response.get("orders", [])
    for order in orders:
        order_id = order.get("id")
        customer_email = order.get("customer", {}).get("email", "No email")
        logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")
    print("Order reminders processed!")
except Exception as e:
    logging.error(f"Error while querying GraphQL: {e}")
    sys.exit(1)
