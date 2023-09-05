import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .apps import MainConfig
import torch


def index(request):
    return render(request, 'main/index.html')


def demo(request):
    return render(request, f'main/demo.html')



@csrf_exempt
def submit(request):

    torch.cuda.empty_cache()
    jsonObject = json.loads(request.body)

    query = jsonObject.get('question')
    top_k = 1
    
    candidate_documents = MainConfig.retriever.retrieve(
        query=query,
        top_k=top_k
    )
    
    context = ""
    for i in range(top_k):
        context += candidate_documents[i].to_dict()['content']+"\n"

    doc_list = []
    for i in range(top_k):
        doc_list.append(candidate_documents[i].to_dict()['meta']['name'])

    try:
        if MainConfig.summarize_before_qa:
            sum_pipe_input = f"### 다음 문서를 요약해줘: {context}\n\n### 요약:"
            summarized = MainConfig.pipe(
                    sum_pipe_input,
                    num_beams=3,
                    # do_sample=True,
                    # temperature=0.7,
                    # top_p=0.9,
                    max_new_tokens=512,
                    return_full_text=False,
                    pad_token_id=MainConfig.pipe.tokenizer.eos_token_id,
                    eos_token_id=2,
                )
            pipe_input = f"### 질문: {query}\n\n### 맥락: {summarized[0]['generated_text']}\n\n### 답변:" if context else f"### 질문: {query}\n\n### 답변:"
        else:
            pipe_input = f"### 질문: {query}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {query}\n\n### 답변:"

        ans_with_qa = MainConfig.pipe(
                pipe_input,
                num_beams=3,
                # do_sample=True,
                # temperature=0.7,
                #top_p=0.9,
                #early_stopping=True,
                max_length=1024,
                #max_new_tokens=2000,
                return_full_text=False,
                pad_token_id=MainConfig.pipe.tokenizer.eos_token_id,
                eos_token_id=2,
            )
    except:    
        [doc_list, doc_page] = doc_list[0].split('pdf_page_')
        
        response = {"answer_response": None,
        "answer_source": None,
        "answer_page": None,
        "answer_document": None}
        torch.cuda.empty_cache()
        return JsonResponse(response)
    
    
    [doc_list, doc_page] = doc_list[0].split('pdf_page_')
    
    response = {"answer_response": ans_with_qa[0]['generated_text'],
    "answer_source": doc_list[len(MainConfig.doc_dir)+1:],
    "answer_page": doc_page[:-4],
    "answer_document": context}
    torch.cuda.empty_cache()

    return JsonResponse(response)