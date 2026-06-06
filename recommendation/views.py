from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .predictor import predict_crop

from groq import Groq
import json


import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@csrf_exempt
def crop_prediction(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            features = [
                float(data["N"]),
                float(data["P"]),
                float(data["K"]),
                float(data["temperature"]),
                float(data["humidity"]),
                float(data["ph"]),
                float(data["rainfall"])
            ]

            crop = predict_crop(features)

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Crop: {crop}

Return ONLY valid JSON.

{{
    "temperature_reason": "",
    "humidity_reason": "",
    "market_reason": ""
}}

Rules:
1. Maximum 5 words each.
2. No markdown.
3. No explanation.
4. Valid JSON only.
"""
                    }
                ]
            )

            groq_response = response.choices[0].message.content

            reasons = json.loads(groq_response)

            return JsonResponse({
                "recommended_crop": crop,
                "temperature_reason": reasons["temperature_reason"],
                "humidity_reason": reasons["humidity_reason"],
                "market_reason": reasons["market_reason"]
            })

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "POST request required"
    }, status=400)


def crop_recommendation(request):
    return render(request, "croprecommendation.html")