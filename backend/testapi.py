import requests

def read_flatten(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return " ".join(content.split())

userstory_raw = read_flatten("userstory-ex.txt")
srs_raw = read_flatten("SRS-ex.txt")

url = "http://127.0.0.1:5000/process_suggestions"
payload = {"userstory_raw": userstory_raw, "srs_raw": srs_raw}
response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())

url2 = "http://127.0.0.1:5000/handle_interaction"
payload2 = {
"userpromt": "Add more clarity to section 3.",
"final_suggestions": response.json(),
"srs_raw": srs_raw
}
response2 = requests.post(url2, json=payload2)
print(response2.status_code)
print(response2.json())

url3 = "http://127.0.0.1:5000/handle_translate"
payload3 = {"text": response2.json()}
response3 = requests.post(url3, json=payload3)
print(response3.status_code)
print(response3.json())
