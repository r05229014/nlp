import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse
from .forms import TextForm
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

def helloworld(request):
    """A test view which tells if the website is working."""
    return HttpResponse('hello world')

def index(request):
    """The only page of text app."""
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            return HttpResponse(handler(input_text=form.cleaned_data['text']))
    form = TextForm()
    context = {
        'form': form
    }
    return render(request, 'text/index.html', context)

def handler(input_text):
    """The Hook of text-handler."""
    # load model
    ws = WS("/home/erica/hololink/data")
    pos = POS("/home/erica/hololink/data")
    ner = NER("/home/erica/hololink/data")

    sentence_list = [input_text]
    word_sentence_list = ws(sentence_list)

    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    
    output = {'Input_text': sentence_list[0]}
    for i, entity in enumerate(entity_sentence_list[0]):
        output[f'Entity_{i}'] = entity
    output_json = json.dumps(output, sort_keys=True, indent=4, ensure_ascii=False)

    # result_text = f'hello world, the text is {input_text}\nentity is {sorted(entity_texts)}'
    return output_json
