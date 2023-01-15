import os
import uuid
from django.views.decorators.csrf import csrf_exempt    # 用来csrf_token验证问题
from django.http import JsonResponse    # 返回json格式的数据
from django.conf import settings    # 配置文件


# 取消掉用于这个方法的身份验证
@csrf_exempt
def upload_file(request):
    # 获取表单上传的图片
    upload = request.FILES.get('upload')    # creditor的表单属性就是upload
    # 生成uuid（随机字符串）
    uid = ''.join(str(uuid.uuid4()).split('-'))
    # 修改图片名称 wzl.jpg -> ['wzgitl', 'jpg']
    names = str(upload.name).split('.')
    names[0] = uid
    # 拼接图片名
    upload.name = '.'.join(names)

    # 构造上传路径
    new_path = os.path.join(settings.MEDIA_ROOT, 'upload/', upload.name)
    # 上传图片
    with open(new_path, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    # 构造要求的数据格式并返回
    filename = upload.name
    url = '/media/upload/' + filename   # 拼接路径
    retdata = {'url': url,
               'uploaded': '1',
               'fileName': filename}
    return JsonResponse(retdata)
