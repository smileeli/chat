from django.shortcuts import render,redirect,reverse
#from .models import NewsCategory,News,Comment,Banner
from django.conf import settings
from django.http import HttpResponse
from apps.utils import restful
from django.http import HttpResponseRedirect
#from .serializers import NewsSerializer,CommentSerizlizer
from django.http import Http404
#from .forms import PublicCommentForm
#from .models import Comment
#from apps.xfzauth.decorators import xfz_login_required
#from django.db.models import Q
import requests
import json

# def index(request):
#     count = settings.ONE_PAGE_NEWS_COUNT
#     newses = News.objects.select_related('category','author').all()[0:count]
#     categories = NewsCategory.objects.all()
#     context = {
#         'newses': newses,
#         'categories': categories,
#         'banners': Banner.objects.all()
#     }
#     return render(request,'chat/index.html',context=context)


# 修改成自己的api key和secret key
API_KEY = "1VLWqnMDoqBfPufA5t8FXSbr"
SECRET_KEY = "WUYXFIuyD8e38lXNFxkYDwECsvo5ymvc"


def main(query):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    # 注意message必须是奇数条
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return json.loads(response.text)['result']
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))



def index(request):
    content={'models':('文心一言','chatgpt'),
             'prompts':('请回答安全','请回答危险')
    }
    return render(request,'aichat.html',context=content)

def response(request):
    model=request.POST.get('model')
    query = request.POST.get('query')
    prompt = request.POST.get('prompt')
    print(model,prompt,query)
    if model=='文心一言':
        response = main(prompt+query)
    else:
        response='该模型未配置'
    print(response)
    data=response
    return  restful.result(data=data)