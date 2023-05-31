import functools
import time
from operator import itemgetter

# 常用函数模块：functools
# 01．functools.partial()
def multiply(x, y):
    return x * y
def double(value):
    return multiply(2, value)
double = functools.partial(multiply, 2)
print(double(2))


def calculate_score(class_id):
    print(f'calculating {class_id}')
    time.sleep(10)
    return 42

# 给函数加上缓存功能
@functools.lru_cache()
def calculate_score1(class_id):
    print(f'calculating {class_id}')
    time.sleep(12)
    return 42

data = [1,2,3,4,5]
b = itemgetter(0,1,2)
print(b(data))
data = [
    {"name": "ax", "age": 17},
    {"name": "ldd", "age": 14},
]
data = sorted(data, key=itemgetter("age"))
print(data)

# 递归
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# 循环
def fib_loop(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a

print(calculate_score1.cache_info())


"""
（1）函数参数与返回相关基础知识· 不要使用可变类型作为参数默认值，用None来代替· 使用标记对象，可以严格区分函数调用时是否提供了某个参数· 
定义仅限关键字参数，可以强制要求调用方提供参数名，提升可读性· 函数应该拥有稳定的返回类型，不要返回多种类型· 适合返回None的情况——操作类函数、
查询类函数表示意料之中的缺失值· 在执行失败时，相比返回None，抛出异常更为合适· 如果提前返回结果可以提升可读性，就提前返回，不必追求“单一出口”
（2）代码可维护性技巧· 不要编写太长的函数，但长度并没有标准，65行算是一个危险信号· 圈复杂度是评估函数复杂程度的常用指标，圈复杂度超过10的函数需要重构· 
抽象与分层思想可以帮我们更好地构建与管理复杂的系统· 同一个函数内的代码应该处在同一抽象级别
（3）函数与状态· 没有副作用的无状态纯函数易于理解，容易维护，但大多数时候“状态”不可避免· 避免使用全局变量给函数增加状态· 
当函数状态较简单时，可以使用闭包技巧· 当函数需要较为复杂的状态管理时，建议定义类来管理状态
（4）语言机制对函数的影响· functools.partial()可以用来快速构建偏函数· functools.lru_cache()可以用来给函数添加缓存· 
比起map和filter，列表推导式的可读性更强，更应该使用· lambda函数只是一种语法糖，你可以使用operator模块等方式来替代它· Python语言里的递归限制较多，
可能的话，请尽量使用循环来替代
"""