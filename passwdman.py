import requests
import json
import string
import random
import sys
from decouple import config

api_key = config('API_KEY')
headers = {"AUTHTOKEN": api_key}

class PasswordManager:

    def __init__(self, headers):
        self.headers = headers

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = random.choice(string.ascii_uppercase)  # Выбор случайной заглавной буквы
        password += random.choice(string.digits)  # Выбор случайной цифры
        password += ''.join(random.choice(characters) for _ in range(12))  # Добавление остальных символов
        return password

    def get_userid(self, user):
        data_request = requests.get(
            f'https://pmp.idfinance.com/restapi/json/v1/user/getUserId?&USERNAME={user}',
            headers=self.headers)
        json_user = data_request.text
        json_loads_user = json.loads(json_user)

        if 'USERID' in json_user and '"status":"Success"' in json_user:
            userid = json_loads_user['operation']['Details']['USERID']
            return userid
        else:
            return 10000000 # Поже нужно переделать на False и добавить проверку в других функциях

    def create_user(self, username, firstname, lastname, email, password):
        input_param = {
            "operation": {
                "Details": {
                    "USERNAME": username,
                    "FIRSTNAME": firstname,
                    "LASTNAME": lastname,
                    "EMAIL": email,
                    "PASSWORD": password,
                    "POLICY": "Strong",
                    "ROLE": "Password User",
                    "ISSUPERADMIN": "false",
                    "DEPARTMENT": "IT",
                    "LOCATION": "Minsk",
                    "ISAPIUSER": "false",
                }
            }
        }

        data = "INPUT_DATA=" + str(input_param)
        data_request = requests.post(
            'https://pmp.idfinance.com/restapi/json/v1/user', headers=self.headers, data=data)
        json_create_user = data_request.text
        json_loads_account = json.loads(json_create_user)
        if '"status":"Success"' in json_create_user:
            status = json_loads_account["operation"]["result"]["message"]
            return status
        else:
            status = json_loads_account["operation"]["result"]["message"]
            return status

    def delete_user(self, user):
        data_request = requests.delete(
            f'https://pmp.idfinance.com/restapi/json/v1/user/{self.get_userid(user)}',
            headers=self.headers)
        json_delete_user = data_request.text
        json_loads_user = json.loads(json_delete_user)

        if '"status":"Success"' in json_delete_user:
            status = json_loads_user["operation"]["result"]["message"]
            return status
        else:
            status = json_loads_user["operation"]["result"]["message"]
            return status

    def get_accountid_resourceid(self, account, resource):
        data_request = requests.get(
            f'https://pmp.idfinance.com/restapi/json/v1/resources/getResourceIdAccountId?RESOURCENAME={resource}&ACCOUNTNAME={account}',
            headers=self.headers)
        json_account_resource = data_request.text
        json_loads_account_resource = json.loads(json_account_resource)

        if 'ACCOUNTID' in json_account_resource and '"status":"Success"' in json_account_resource:
            account_id = json_loads_account_resource['operation']['Details']['ACCOUNTID']
            resource_id = json_loads_account_resource['operation']['Details']['RESOURCEID']
            return account_id, resource_id

        else:
            return (1000000, 1000000) # Позже нужно переделать на False и добавить проверку в других функциях

    def get_resource_id(self, name):
        data_request = requests.get(
            f'https://pmp.idfinance.com/restapi/json/v1/resources/resourcename/{name}',
            headers=self.headers)
        json_resource = data_request.text
        json_loads_resource = json.loads(json_resource)

        if '"status":"Success"' in json_resource:
            resource_id = json_loads_resource["operation"]["Details"]["RESOURCEID"]
            return resource_id
        else:
            return 1000000 # Поже нужно переделать на False и добавить проверку в других функциях

    def create_account_under_resource(self, account, resource, password):
        input_param = {
            "operation": {
                "Details": {
                    "ACCOUNTLIST": [
                        {
                            "ACCOUNTNAME": account,
                            "PASSWORD": password
                        }
                    ]
                }
            }
        }
        data = "INPUT_DATA=" + str(input_param)
        data_request = requests.post(
            f'https://pmp.idfinance.com/restapi/json/v1/resources/{self.get_resource_id(resource)}/accounts',
            headers=self.headers, data=data)
        json_create_account_resource = data_request.text
        json_loads_account_resource = json.loads(json_create_account_resource)

        if '"STATUS":"Account added successfully"' in json_create_account_resource:
            status = json_loads_account_resource["operation"]["result"]["message"]
            return account + " " + status
        elif '"STATUS":"Account is not added  as it already exists"' in json_create_account_resource:
            status = json_loads_account_resource['operation']['Details'][0][account]['STATUS']
            return status
        else:
            status = json_loads_account_resource["operation"]["result"]["message"]
            return status

    def edit_cred_account_under_resource(self, account, resource, password):
        input_param = {
            "operation": {
                "Details": {
                    "NEWPASSWORD": password,
                    "RESETTYPE": "LOCAL",
                    "REASON": "Password Expired"
                }
            }
        }
        data = "INPUT_DATA=" + str(input_param)
        resource_id = self.get_accountid_resourceid(account, resource)[1]
        account_id = self.get_accountid_resourceid(account, resource)[0]
        data_request = requests.put(
            f'https://pmp.idfinance.com/restapi/json/v1/resources/{resource_id}/accounts/{account_id}/password',
            headers=self.headers, data=data)
        json_edit_account = data_request.text
        json_loads_account = json.loads(json_edit_account)

        if '"status":"Success"' in json_edit_account:
            status = json_loads_account["operation"]["result"]["message"]
            return status
        elif '"status":"Failed"' in json_edit_account and 'No such account found' in json_edit_account:
            return self.create_account_under_resource(account, resource, password)
        else:
            status = json_loads_account["operation"]["result"]["message"]
            return status

    def share_account_to_user(self, account, resource, user):
        userid = self.get_userid(user)
        input_param = {
            "operation": {
                "Details": {
                    "ACCESSTYPE": "view",
                    "USERID": userid
                }
            }
        }
        data = "INPUT_DATA=" + str(input_param)
        resource_id = self.get_accountid_resourceid(account, resource)[1]
        account_id = self.get_accountid_resourceid(account, resource)[0]
        data_request = requests.put(
            f'https://pmp.idfinance.com/restapi/json/v1/resources/{resource_id}/accounts/{account_id}/share',
            headers=self.headers, data=data)
        json_share_account = data_request.text
        json_loads_account = json.loads(json_share_account)
        if '"status":"Success"' in json_share_account:
            status = json_loads_account["operation"]["result"]["message"]
            return status
        else:
            status = json_loads_account["operation"]["result"]["message"]
            return status


if __name__ == "__main__":
    # Получение аргументов командной строки
    password_manager = PasswordManager(headers)
    generated_password = password_manager.generate_password()
    function_choice = sys.argv[1] if len(sys.argv) > 1 else "default_function"
    headers = {"AUTHTOKEN": api_key}

    if function_choice == "-edit":
        account = sys.argv[2]
        resource = sys.argv[3]
        passwd = sys.argv[4] if len(sys.argv) > 4 else generated_password
        result = password_manager.edit_cred_account_under_resource(account, resource, passwd)

    elif function_choice == "-share":
        account = sys.argv[2]
        resource = sys.argv[3]
        user = sys.argv[4]
        result = password_manager.share_account_to_user(account, resource, user)

    elif function_choice == "-create_account":
        account = sys.argv[2]
        resource = sys.argv[3]
        passwd = sys.argv[4] if len(sys.argv) > 4 else generated_password
        result = password_manager.create_account_under_resource(account, resource, passwd)

    elif function_choice == "-create_user":
        username = sys.argv[2]
        firstname = sys.argv[3]
        lastname = sys.argv[4]
        email = sys.argv[5]
        passwd = sys.argv[6] if len(sys.argv) > 6 else generated_password
        result = password_manager.create_user(username, firstname, lastname, email, passwd)

    elif function_choice == "-delete_user":
        username = sys.argv[2]
        result = password_manager.delete_user(username)

    else:
        result = "Invalid function choice"

    print(result)
