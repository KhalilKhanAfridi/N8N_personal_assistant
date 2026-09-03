import requests

user_message = "create an event titled 'test' tomorrow 9/4/2026 at 6:00PM with time zone Asia/Karachi.use create event calender tool."


request_message = {"message" : user_message}

url = "https://khalilkhanafridi.app.n8n.cloud/webhook-test/59209596-e40b-459c-9c56-ee770cce2a32"

response = requests.post(url, json=request_message)

print(response.status_code)

result = response.json()[0]["output"]
print(result)