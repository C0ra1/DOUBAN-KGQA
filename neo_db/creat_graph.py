from py2neo import Graph, Node, Relationship,NodeMatcher
from config import graph
# 用于生成图数据库
with open("./raw_data/relation.txt",'rb') as f:
    for line in f.readlines():
        line = line.decode()
        # 以,隔开，去除换行符
        rela_array=line.strip("\n\r").split("*")
        print(rela_array)
        tags_list = ['小说','编程','web','算法','神经网络','科技','名著','推理','悬疑','青春','言情','校园','经济','漫画','散文','其他']
        if rela_array[3] in tags_list:
            type1 = 'Book'
        elif rela_array[3] == '分类':
            type1 = 'Category'
        elif rela_array[3] == '出版年份':
            type1 = 'Date'
        else:
            type1 = 'Person'
        graph.run("MERGE(p: %s{cate:'%s',Name: '%s'})" % (type1, rela_array[3], rela_array[0]))
        if rela_array[4] in tags_list:
            type2 = 'Book'
        elif rela_array[4] == '分类':
            type2 = 'Category'
        elif rela_array[4] == '出版年份':
            type2 = 'Date'
        else:
            type2 = 'Person'
        graph.run("MERGE(p: %s{cate:'%s',Name: '%s'})" % (type2, rela_array[4], rela_array[1]))
        graph.run(
            "MATCH(e: %s), (cc: %s) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (type1, type2, rela_array[0], rela_array[1], rela_array[2], rela_array[2])

        )
        
