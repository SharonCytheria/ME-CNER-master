import pickle

fr = open('test.pkl', 'rb')  # open的参数是pkl文件的路径

loadData = pickle.load(fr)  # 读取pkl文件的内容
# print("----type----")
# print(type(loadData))
print("----data----")
print(loadData)
fr.close()  # 关闭文件