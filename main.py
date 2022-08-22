import json
import logging

import requests
from requests.exceptions import HTTPError

from helper_functions import convert_xml_to_dict, xml_validator, pascal_to_snake


logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class Order:
    def __init__(self, order_url, menu_url, xml_file, schema_validator_file):
        self.order_url = order_url
        self.menu_url = menu_url
        self.xml_file = xml_file
        self.schema_validator_file = schema_validator_file

    def get_menu(self):
        try:
            response = requests.get(self.menu_url)
        except HTTPError as http_err:
            logging.info(f"HTTP error occurred: {http_err}")

        return response.json()

    def place_order(self, data):
        try:
            response = requests.post(url=self.order_url, data=data)
        except HTTPError as http_err:
            logging.info(f"HTTP error occurred: {http_err}")
        return response.text

    def get_item_id_from_menu(self, menu, item_name):
        items = menu["dishes"]
        for item in items:
            if item["name"] == item_name:
                return item["id"]

    def order_from_menu(self, order):
        orders_list = []
        order_item = order.split(", ")

        for item in order_item:
            item_info = item.split(" ", 1)
            item_name = item_info[1:][0]
            menu = self.get_menu()
            item_id = self.get_item_id_from_menu(menu, item_name)
            quantity = item[0]
            orders_list.append({"id": item_id, "amount": int(quantity)})
        return orders_list

    def order(self):
        valid_schema = xml_validator(self.xml_file, self.schema_validator_file)
        if valid_schema:
            employee_dict = convert_xml_to_dict(self.xml_file)
        else:
            return {"Result": "Schema is not valid"}

        employee_info = employee_dict["Employees"]["Employee"]
        order_dict = {"orders": []}

        for employee in employee_info:
            if employee["IsAttending"] == "true":
                each_order = {"customer": {}, "items": []}

                customer_name = employee["Name"]
                address = employee["Address"]
                customer_address = {
                    pascal_to_snake(key): value for key, value in address.items()
                }
                order = employee["Order"]
                customer_order = self.order_from_menu(order)

                each_order["customer"]["name"] = customer_name
                each_order["customer"]["address"] = customer_address
                each_order["items"] = customer_order

                order_dict["orders"].append(each_order)

        json_data = json.dumps(order_dict)
        order_completion_status = self.place_order(json_data)
        return order_completion_status


if __name__ == "__main__":
    order_url = "http://nourish.me/api/v1/bulk/order"
    menu_url = "https://nourish.me/api/v1/menu"
    xml_file = "add-path-of-the-xml-file-here"
    schema_validator_file = "schema.xsd"
    Order(order_url, menu_url, xml_file, schema_validator_file).order()
