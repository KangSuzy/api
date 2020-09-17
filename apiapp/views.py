from django.shortcuts import render,get_object_or_404, redirect
from .forms import BoardForm
from .models import Board
from django.utils import timezone
import requests
import json

# Create your views here.

def post(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit = False)
            board.update_date = timezone.now()
            board.save()
            return redirect('show')
    else:
        form = BoardForm()
        return render(request,'post.html', {'form':form})

def edit(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit = False)
            board.update_date = timezone.now()
            board.save()
            return redirect('show')
    else:
        form = BoardForm(instance=board)
        return render(request,'post.html', {'form':form})

        
def show(request):
    boards = Board.objects.order_by('-id') #최신순정렬
    return render(request, 'show.html',{'boards':boards})

def detail(request, board_id):
    board_detail = get_object_or_404(Board, pk=board_id)
    return render(request, 'detail.html', {'board':board_detail})

def delete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('show')

# Kakao api
url = "https://dapi.kakao.com/v2/search/web"
queryString = {"query" : "덕성여자대학교"}
header = {"Authorization":"KakaoAK 0b251c77a3d989e136e64cc26a3ddb05"}
r = requests.get(url, headers=header, params = queryString)
print(json.loads(r.text))