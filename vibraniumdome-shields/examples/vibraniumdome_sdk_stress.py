import os
import openai
import time
import concurrent.futures
from vibraniumdome_sdk import VibraniumDome

openai.api_key = os.getenv("OPENAI_API_KEY")

app_name = "playground"
# app_name="insurance_quote"
# app_name="gpt_next"
# app_name="app.legal.chat"
used_id = "user-123456"
# used_id = "user-456789"
session_id_header = "cdef-1234-abcd"
# session_id_header = "abcd-1234-cdef"

VibraniumDome.init(app_name=app_name)


def query_openai():
    """
    Function to perform a single query to the OpenAI service.
    This function now returns a tuple (success: bool, response_or_error: str).
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"},
            ],
            temperature=0,
            request_timeout=30,
            user=used_id,
            headers={"x-session-id": session_id_header},
        )
        print(response)
        return (True, response.choices[0].message.content)
    except Exception as e:
        return (False, str(e))


def run_stress(duration_seconds=60, concurrent_requests=10):
    """
    Main function to measure the throughput of service over a specified duration in seconds,
    tracking and printing the number of failed requests and responses.

    :param duration_seconds: Duration to run the test for, in seconds.
    :param concurrent_requests: Number of concurrent requests to simulate.
    """
    start_time = time.time()
    end_time = start_time + duration_seconds
    successful_queries = 0
    failed_queries = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        while time.time() < end_time:
            futures = [executor.submit(query_openai) for _ in range(concurrent_requests)]
            for future in concurrent.futures.as_completed(futures):
                success, response_or_error = future.result()
                if success:
                    successful_queries += 1
                else:
                    failed_queries += 1
                    print(f"Failed response: {response_or_error}")

    total_time = time.time() - start_time

    print(f"Successfully completed {successful_queries} requests in {total_time:.2f} seconds.")
    print(f"Failed requests: {failed_queries}")
    if total_time > 0:
        print(f"Queries per second (QPS): {successful_queries / total_time:.2f}")
    else:
        print("No time elapsed, can't calculate QPS.")


if __name__ == "__main__":
    run_stress(60, 2)
