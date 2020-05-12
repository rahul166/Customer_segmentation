import urllib.request
import json

# data = {
#         "Inputs": {
#                 "input1":
#                 [
#                     {
#                             'Column 0': "1",   
#                             'CustomerID': "1",   
#                             'amount_log': "1",   
#                             'recency_log': "1",   
#                             'frequency_log': "1",   
#                     }
#                 ],
#         },
#     "GlobalParameters":  {
#     }
# }



url = 'https://ussouthcentral.services.azureml.net/workspaces/c99d0172d66d43ec8073e6de0e90f4c9/services/8cae2d1b40174345bb10b33c6bc6aad6/execute?api-version=2.0&format=swagger'
api_key = 'abcd' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

def main_func(transformed):


    data = {
        "Inputs": {
                "input1":
                [
                    {
                            'Column 0': "1",   
                            'CustomerID': "1",   
                            'amount_log': transformed[0][0],   
                            'recency_log': transformed[0][1],   
                            'frequency_log':transformed[0][2],   
                    }
                ],
        },
    "GlobalParameters":  {
        }
    }
    body = str.encode(json.dumps(data))

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        # print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
