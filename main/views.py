import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rouge import Rouge
from datasets import load_metric
from main import eda

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def demo(request):
    return render(request, f'main/demo.html')


rouge = Rouge()
bertscore_metric = load_metric('bertscore')


@csrf_exempt
def submit(request):
    jsonObject = json.loads(request.body)
    reference = jsonObject.get('gold')

    aug_sent = eda.eda_function(sentence=reference)

    r = []
    b = []
    for i in range(3):
        score = rouge.get_scores(aug_sent[i], reference)
        r.append(round(score[0]["rouge-l"]["f"]*100))

        bert_score = bertscore_metric.compute(predictions=[aug_sent[i]], references=[reference], lang="en")
        b.append(round(bert_score["f1"][0]*100))

    response = {"ex": aug_sent, "rouge_score": r, "bert_score": b}
    return JsonResponse(response)
