from django.shortcuts import render
from django.http import JsonResponse
from .rag import ask_paddy_bot
import json

def chatbot(request):

    if request.method == "POST":

        try:

            data = json.loads(
                request.body
            )

            question = data.get(
                "question",
                ""
            )

            history = data.get(
                "history",
                []
            )

            answer = ask_paddy_bot(
                question,
                history
            )

            return JsonResponse(
                {
                    "answer": answer
                }
            )

        except Exception as e:

            return JsonResponse(
                {
                    "answer": str(e)
                },
                status=500
            )

    return JsonResponse(
        {
            "error": "Invalid Request"
        },
        status=400
    )








def index(request):
    return render(request, "chatbot.html")