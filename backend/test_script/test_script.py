import requests
import json

from test_data import test_data

django_url = "http://localhost:8000"


def test_post_request(comment, data):
    url = f"{django_url}/get_form/"
    response = requests.post(url, json=data)

    try:
        if response.status_code == 200:
            print(
                json.dumps(
                    {
                        "comment": comment,
                        "request_body": data,
                        "response": response.json(),
                    },
                    indent=2,
                )
            )
            print("\n")
    except Exception as e:
        print(f"\n Ошибка {e} при запросе с данными: {data}")
        print(response.text)


if __name__ == "__main__":
    for test_case in test_data:
        test_post_request(test_case["comment"], test_case["test_data"])
