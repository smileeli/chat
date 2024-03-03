from django.shortcuts import render,redirect,reverse
from django.conf import settings
from django.http import HttpResponse
from apps.utils import restful
from django.http import HttpResponseRedirect
from .models import Infer,Llmodel,Thread,Textname
from django.http import Http404
import requests
import json
from django.db.models import Q
import os
from django.http import StreamingHttpResponse


def save_file(file,path):
    with open(path, 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

def index(request):
    infers = Infer.objects.all()
    text_files=Textname.objects.all()
    models=Llmodel.objects.all()
    threads=Thread.objects.all()
    print(infers)
    args={'models':('文心一言','chatgpt'),
             'text_files':('测试集1','测试集2'),
             'types':('common', 'greed'),
             'prompt_types':('safe', 'unsafe'),
             'thread_nums':(4,10,20),
             'parameters':('模型','测试集','线程数量')
    }
    return render(request,'infer.html',context={'infers':infers,'text_files':text_files,'args':args,'models':models
                                                ,'threads':threads})


def add_args(request):
    parameter = request.POST.get('parameter')
    content = request.POST.get('content')
    print(parameter)
    if parameter=='模型':
        models=list(Llmodel.objects.values_list('name',flat=True))
        if content not in models:
            table=Llmodel(name=content)
            table.save()
            return restful.result(data='已添加')
        else:
            return restful.result(data='请不要重复添加')
    elif parameter=='线程数量':
        threads = list(Thread.objects.values_list('num', flat=True))
        if content not in threads:
            table = Thread(num=content)
            table.save()
            return restful.result(data='已添加')
        else:
            return restful.result(data='请不要重复添加')
    else:
        print('111')
        myfile = request.FILES.get('myfile')
        filename=myfile.name
        print(filename)
        path = os.path.join(settings.MEDIA_ROOT, 'test', filename + '.txt')
        save_file(myfile,path)
        return HttpResponse('success')

def add_args2(request):
    myfile = request.FILES.get('myfile',None)
    filename = myfile.name
    print(filename)
    path = os.path.join(settings.MEDIA_ROOT, 'test', filename)
    save_file(myfile, path)
    table = Textname(name=filename)
    table.save()
    return HttpResponse('success')


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

def begain_infers(request):
    id = request.POST.get('infer_id')
    infer=Infer.objects.get(id=id)
    file=infer.file
    path=os.path.join(settings.MEDIA_ROOT,'test',file+'.txt')
    result_path=os.path.join(settings.MEDIA_ROOT,'result',id+'.json')
    if os.path.exists(result_path):
        os.remove(result_path)
    print(path)
    infer = Infer.objects.get(id=id)
    with open(path, 'r', encoding='utf-8') as fd:
        contents=fd.readlines()
        lengs=len(contents)
        for i in range(lengs):
            print(contents[i])
            data=json.loads(contents[i])
            print(data)
            infer.status=str(round((i+1)/lengs)*100)+'%'
            infer.save()
            prompt=data['prompt']
            response = main(prompt)
            print(response)
            with open(result_path, 'a+', encoding='utf-8') as fd2:
                dicts = dict(prompt=prompt, response=response)
                fd2.write(json.dumps(dicts,ensure_ascii=False))
                fd2.write('\n')
    return restful.result(data='完成')

def add_infers(request):
    name = request.POST.get('name')
    file = request.POST.get('file')
    type = request.POST.get('type')
    prompt = request.POST.get('prompt')
    status = request.POST.get('status')
    thread = request.POST.get('thread')
    print(name)
    if Infer.objects.filter(Q(name=name) & Q(file=file)):
        return restful.result(data='请勿重复提交任务')
    else:
        table=Infer(name=name,file=file,type=type,prompt=prompt,status=status,thread=thread)
        table.save()
        return restful.result(data='已添加')

def delete_infers(request):
    id = request.POST.get('infer_id')
    infer=Infer.objects.get(id=id)
    infer.delete()
    return restful.result(data='已删除')

def change_status(request):
    id = request.POST.get('infer_id')
    infer=Infer.objects.get(id=id)
    infer.status = '等待中...'
    infer.save()
    return restful.result(data='已更新')

def download(request):
    id = request.POST.get('orderid')
    # infer = Infer.objects.get(id=id)
    # id = request.POST.get('infer_id')
    print(id)
    file_name = id+'.json'
    result_path = os.path.join(settings.MEDIA_ROOT,'result',file_name)
    file = open(result_path, 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name.encode('utf-8').decode('ISO-8859-1'))
    return response
