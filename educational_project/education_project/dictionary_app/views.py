from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dictionary(request):
    file = open("dictionary_app/local_dict.txt", "r", encoding="utf-8").read().splitlines()
    words1 = []
    words2 = []
    for line in file:
        word1, word2 = line.split("-")
        words1.append(word1)
        words2.append(word2)

    return render(request, 'dictionary_app/dict.html', context={'words_1': words1, 'words_2': words2})
    # return HttpResponse("Hi, this is dictionary_app")


def index(request):
    # return HttpResponse("Hi, this is dictionary_app")
    return render(request, 'dictionary_app/index.html', context={'title': 'My dictionary'})


def add_word(request):
    if request.method == 'POST':
        with open("dictionary_app/local_dict.txt", "a", encoding='utf-8') as file:
            file.write(request.POST['word1'] + "-" + request.POST['word2'] + '\n')
        return render(request, 'dictionary_app/add_word.html')
    return render(request, 'dictionary_app/add_word.html')
