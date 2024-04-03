from greenlet import greenlet

def func1():
    print(1)      # 第二步 输出1
    gr2.switch()  # 第三步 切换func2函数
    print(2)      # 第六步 输出2
    gr2.switch()  # 第七步 切换func2函数

def func2():
    print(3)       # 第四步 输出3
    gr1.switch()   # 第五步 切换func1函数
    print(4)       # 第八步 输出4
    gr1.switch()   # 第九步 切换func1函数

gr1 = greenlet(func1)
gr2 = greenlet(func2)
gr1.switch()     # 第一步 去执行func1函数
