import codecs
# 获取人物数组
def get_character():
    f = codecs.open('./raw_data/relation.txt','r','utf-8')
    data = []
    for line in f.readlines():
        array = line.strip("\n").split(",")
        arr = [array[0],array[1]]
        data.extend(arr)
    
    return data

