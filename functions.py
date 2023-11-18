import json


def call_function(messages, function_call):
    """Function calling function which executes function calls when the model believes it is necessary.
    Currently extended by adding clauses to this if statement."""
    print(function_call)

    if function_call["name"] == "order_tracking_status":
        try:
            parsed_output = json.loads(
                function_call["arguments"]
            )
            print("Looking up order status")
            results = get_order_tracking_status(parsed_output["email_address"], parsed_output["order_number"])
            return {
                    "role": "function",
                    "name": function_call["name"],
                    "content": str(results),
                }
        except Exception as e:
            # print(parsed_output)
            print(f"Function execution failed")
            print(f"Error message: {e}")
            return {"role": "function", "content": "call failed", "name": "order_tracking_status"}
        # try:
        #     print("Got search results, summarizing content")
        #     response = chat_completion_request(messages)
        #     return response.json()
        # except Exception as e:
        #     print(type(e))
        #     raise Exception("Function chat request failed")

    # elif (
    #     full_message["message"]["function_call"]["name"] == "read_article_and_summarize"
    # ):
    #     parsed_output = json.loads(
    #         full_message["message"]["function_call"]["arguments"]
    #     )
    #     print("Finding and reading paper")
    #     summary = summarize_text(parsed_output["query"])
    #     return summary

    else:
        raise Exception("Function does not exist and cannot be called")

def get_order_tracking_status(email_address, order_number):
    return "The order was delivered on Monday, November 12th"