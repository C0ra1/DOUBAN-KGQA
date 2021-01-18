from neo_db.config import graph, CA_LIST, similar_words
from spider.show_profile import get_profile
from urllib import request
import codecs
from PIL import Image
import os
import json
import base64
# KGQA关键代码
# 根据名字单独查找
def query(name, method):
    if method == 'true':
        data = graph.run(
            "match(p)-[r]->(n) where n.Name =~ '.*%s.*' return p.Name,r.relation,n.Name,p.cate,n.cate\
                Union all\
            match(p) -[r]->(n) where p.Name =~ '.*%s.*' return p.Name, r.relation, n.Name, p.cate, n.cate\
            "
            % (name,name)
        )
        data = list(data)
        return get_json_data(data)
    elif method == 'false':
        data = graph.run(
            "match(p)-[r]->(n) where n.Name =~ '%s' return p.Name,r.relation,n.Name,p.cate,n.cate\
                Union all\
            match(p) -[r]->(n) where p.Name =~ '%s' return p.Name, r.relation, n.Name, p.cate, n.cate\
            "
            % (name,name)
        )
        data = list(data)
        return get_json_data(data)
    
def get_json_data(data):
    json_data={'data':[],"links":[],"code":0}
    d=[]

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name']+"_"+i['p.cate'])
        d.append(i['n.Name']+"_"+i['n.cate'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        j_array[1] = j_array[1].strip()
        data_item['category']=CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.Name']]
        
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)
    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))

# 输入问句，KGQA给出结果
def get_KGQA_answer(array):
    data_array=[]
    result = '默认'
    tags_list = ['小说','编程','web','算法','神经网络','科技','名著','推理','悬疑','青春','言情','校园','经济','漫画','散文','其他']
    for i in range(len(array)-2):
        if i==0:
            name=array[0]
        else:
            # 下标为-1代表输出最后一个数
            name=data_array[-1]['p.Name']
        # 在数据库中查找以name为头实体，array[i+1]为关系的尾实体
        data = graph.run(
        "match(p)-[r]->(n) where r.relation =~ '.*%s.*' and (n.Name =~ '.*%s.*' or p.Name =~ '.*%s.*') return p.Name,n.Name,r.relation,p.cate,n.cate\
        "
        % (similar_words[array[i+1]], name, name)
        )
        # data是查询出来的结果，包含两个实体、实体的属性以及关系
        # list()将元组转化为列表
        data = list(data)
        # data_array储存查出来的所有路径上的实体
        data_array.extend(data)

    if str(data_array[-1]['p.cate']) in tags_list:
        result = str(data_array[-1]['p.Name'])
    else:
        result = '默认'
    # 打开json查找图片地址
    with open('./spider/json/data.json', encoding='utf-8')as f:
        data = json.load(f)
        img_url = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1802553443,2497346274&fm=26&gp=0.jpg'
        for i in data[result]:
            if str(i) == "图片链接":
                img_url = str(data[result][i])
                break
        # 将图片保存到本地
        request.urlretrieve(img_url, './spider/images/'+'%s.jpg' % (result))

    # with expression [as target]:
    # expression是一个需要执行的表达式
    # target是一个变量或元组，储存的是expression表达式执行返回的结果
    # 打开对应的图片
    with open("./spider/images/"+"%s.jpg" % (result), "rb") as image:
        # print(str(data_array[-1]['p.Name']))
        # 读取图片存入base64_data变量
        base64_data = base64.b64encode(image.read())
        # 转化为字符串
        b=str(base64_data)
    # get_json_data() 返回json格式的data_array
    # get_profile() 返回查出答案的详细信息
    # 返回一个数组，包含查出来的所有路径上的实体，查出实体的详细信息，查出实体的图片
    # str(data_array[-1]['p.Name'])是查出来的目标结果对于的名字，如"贾宝玉"
    return [get_json_data(data_array), get_profile(result), b.split("'")[1]]

# 返回name的详细信息
def get_answer_profile(name):
    # result是要查的名字
    result = str(name)
    # 打开json查找图片地址
    with open('./spider/json/data.json', encoding='utf-8')as f:
        data = json.load(f)
        img_url = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1802553443,2497346274&fm=26&gp=0.jpg'
        try:
            for i in data[name]:
                if str(i) == "图片链接":
                    img_url = str(data[name][i])
                    break
        except:
            print('fxk')
        # 将图片保存到本地
        request.urlretrieve(img_url, './spider/images/'+'%s.jpg' % (result))

    with open("./spider/images/"+"%s.jpg" % (result), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]

        



