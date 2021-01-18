import csv
import requests


def auth():
    print("Enter Twitter API Bearer token:")
    return input()


def create_url(next_token):
    print("(press enter to execute standard/test query)\nEnter your search query:")
    query_input = input()
    if query_input == "\n" or query_input == "":
        query = "(student OR studeren OR universiteit OR hogeschool OR tentamen) maastricht"
    max_results = "100"
    tweet_fields = "public_metrics"
    if next_token is None:
        return "https://api.twitter.com/2/tweets/search/recent?max_results={}&tweet.fields={}&query={}".format(
            max_results,
            tweet_fields,
            query
        )
    else:
        return "https://api.twitter.com/2/tweets/search/recent?max_results={}&next_token={}&tweet.fields={}&query={}".format(
            max_results,
            next_token,
            tweet_fields,
            query
        )


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(headers, next_token):
    url = create_url(next_token)
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    json_response = response.json()
    if "next_token" in json_response["meta"]:
        return response.json(), json_response["meta"]["next_token"]
    return response.json(), None


def calculate_score(response):
    score = 0
    for key, value in response.items():
        score += value
    print(score)
    return score


def main():
    bearer_token = auth()
    headers = create_headers(bearer_token)
    tweet_data = []
    next_token = None
    has_next = True
    while has_next:
        response = connect_to_endpoint(headers, next_token)
        for tweet in response[0]["data"]:
            tweet_data.append({"id": tweet["id"], "interactions": calculate_score(tweet["public_metrics"])})
        print(tweet_data)
        next_token = response[1]
        if next_token is None:
            has_next = False
    with open('output.csv', mode='w', newline='') as output:
        fieldnames = ['id', 'interactions']
        output_writer = csv.DictWriter(output, fieldnames=fieldnames)
        output_writer.writeheader()
        for row in tweet_data:
            output_writer.writerow(row)
            print(row)


if __name__ == "__main__":
    main()
