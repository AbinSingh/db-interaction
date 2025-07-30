

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def handle_question(question, account):
    # Your logic: search, scrape, GPT call
    print(f"[{account}] Answering: {question}")
    time.sleep(1)  # Simulate delay

def process_requests():
    from routers import request_queue # # avoid circular import
    while True:
        request = request_queue.get()
        print(f"Processing for account: {request['account']}")

        questions = request["questions"]
        account = request["account"]

        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(handle_question, q, account): q for q in questions}

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error processing question {futures[future]}: {e}")

        print(f"Finished processing for account: {account}")
        request_queue.task_done()


