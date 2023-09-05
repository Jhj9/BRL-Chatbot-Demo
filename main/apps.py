from django.apps import AppConfig

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"
import logging
import torch
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from transformers import GenerationConfig, AutoModelForQuestionAnswering, AutoTokenizer, pipeline, AutoModelForCausalLM, AutoConfig
from haystack.nodes import BM25Retriever, EmbeddingRetriever
from haystack.utils import print_answers
from accelerate import init_empty_weights, load_checkpoint_and_dispatch, infer_auto_device_map, dispatch_model
from accelerate.utils import get_balanced_memory

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    summarize_before_qa = False
    bm25 = False

    # logger 설정
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
    logging.getLogger("haystack").setLevel(logging.INFO)

    completion_model_name = 'beomi/KoAlpaca-Polyglot-12.8B'
    generation_config = GenerationConfig.from_pretrained(completion_model_name)
    

    doc_dir = os.getcwd()+"/data"
    files_to_index = [os.getcwd()+"/data" + '/' + f for f in os.listdir(doc_dir)]

    meta_file_list = [dict(name=file) for file in files_to_index]

    # 1: Retriever
    if bm25:
        document_store = InMemoryDocumentStore(use_bm25=True)
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index, meta=meta_file_list)
        retriever = BM25Retriever(document_store=document_store)
    else:
        document_store = InMemoryDocumentStore(embedding_dim=1024)
        indexing_pipeline = TextIndexingPipeline(document_store)
        indexing_pipeline.run_batch(file_paths=files_to_index, meta=meta_file_list)
        retriever = EmbeddingRetriever(document_store=document_store, 
                                embedding_model='intfloat/multilingual-e5-large', 
                                model_format="sentence_transformers")
        document_store.update_embeddings(retriever)

    try:
        config = AutoConfig.from_pretrained(completion_model_name)
        with init_empty_weights():
            completion_model = AutoModelForCausalLM.from_config(config).half()
        #"balanced_low_0"
        completion_model = load_checkpoint_and_dispatch(completion_model, checkpoint="/brl/"+completion_model_name, device_map="balanced_low_0", no_split_module_classes=["GPTNeoXLayer", "GPTNeoXMLP"])
    except:
        completion_model = AutoModelForCausalLM.from_pretrained(completion_model_name)
        completion_model.save_pretrained('/brl/'+completion_model_name)
        config = AutoConfig.from_pretrained(completion_model_name)
        with init_empty_weights():
            completion_model = AutoModelForCausalLM.from_config(config).half()
        #"balanced_low_0"
        completion_model = load_checkpoint_and_dispatch(completion_model, checkpoint="/brl/"+completion_model_name, device_map="balanced_low_0", no_split_module_classes=["GPTNeoXLayer", "GPTNeoXMLP"])
    
    completion_model.eval()

    pipe = pipeline(
        'text-generation', 
        model=completion_model,
        tokenizer=completion_model_name,
        #device=device
    )
    