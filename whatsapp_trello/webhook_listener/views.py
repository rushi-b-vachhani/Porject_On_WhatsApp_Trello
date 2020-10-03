from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from nltk.tokenize import LineTokenizer
import re
import requests


def createBoard(board_name):
    url = "https://api.trello.com/1/boards/"
    query = {
        'key': '4a5dbc50f155214b02383022040f44c1',
        'token': '22d37c761a767cb486a0bbe3b976aff4d83cbe497acfef974104b4b5828dc6a5',
        'name': board_name
    }
    response = requests.request(
        "POST",
        url,
        params=query
    )
    print(query)
    print(response.text)

def process_command(command):
    if(re.findall(r"^@\w*\-\w+$", command)):
        command_parameters = re.findall(r"[^@-][\w]*", command)
        if(command_parameters[0].lower() == "createboard"):
            createBoard(command_parameters[1])
        else:
            print("Command unidentified: " + command)
    else:
        print("Invalid Command: " + command)
    

def lineTokenize(data):
    lineTokenize_object = LineTokenizer()
    lineTokenize_string = lineTokenize_object.tokenize(data) 
    return(lineTokenize_string)

@csrf_exempt
@require_POST
def webhook_listener_with_response(request):
    if request.method == 'POST':
        data = request.POST.get("Body",default = None)
        print("Data received: " + data)
        lineTokenize_string = lineTokenize(data)
        for single_line_from_data in lineTokenize_string:
            if(re.search("^@.*", single_line_from_data)):
                process_command(single_line_from_data)
            else:
                print("Not a command: " + single_line_from_data)



    return HttpResponse(str(request.META))

# Create your views here.
