from opensearchpy import OpenSearch

host = "localhost"
port = 9200
auth = ("admin", "admin")

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

document = {
    "id": "ad96f58f624104f3a9cb3003b606cc36",
    "start_time_unix_nano": 1698944869118837000,
    "end_time_unix_nano": 1698944870464491000,
    "llm_vendor": "OpenAI",
    "llm_api_base": "https://api.openai.com/v1",
    "llm_api_type": "open_ai",
    "llm_request_type": "chat",
    "llm_request_model": "gpt-3.5-turbo",
    "llm_response_model": "gpt-3.5-turbo-0613",
    "llm_usage": {"prompt_tokens": 53, "completion_tokens": 17, "total_tokens": 70},
    "llm_prompts": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"},
    ],
    "llm_completions": [{"finish_reason": "stop", "role": "assistant", "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas."}],
}

index_name = "vibranium_index"
response = client.index(index=index_name, body=document, id=document["id"], refresh=True)

print(response)

search_response = client.search(index=index_name, body={"query": {"match": {"title": "Test Document"}}})

print(search_response)
