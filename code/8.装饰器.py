import functools
import time
from functools import wraps


@functools.lru_cache
def function():
    pass

# 完全等同于下面这样：
def function1():
    pass
function1 = functools.lru_cache(function1)

"""
装饰器并不提供任何独特的功能，它所做的，只是让我们可以在函数定义语句上方，直接添加用来修改函数行为的装饰器函数。
假如没有装饰器，我们也可以在完成函数定义后，手动做一次包装和重新赋值。
但正是因为装饰器提供的这一丁点儿好处，“通过包装函数来修改函数”这件事变得简单和自然起来。
"""

def timer(print_args=False):
    """装饰器：打印函数耗时

    :param print_args: 是否打印方法名和参数，默认为 False
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            st = time.perf_counter()
            ret = func(*args, **kwargs)
            if print_args:
                print(f'"{func.__name__}", args: {args}, kwargs: {kwargs}')
            print('time cost: {} seconds'.format(time.perf_counter() - st))
            return ret

        return wrapper

    return decorator


def calls_counter(func):
    """装饰器：记录函数被调用了多少次

    使用func.print_counter() 可以打印统计到的信息
    """
    counter = 0

    def decorated(*args, **kwargs):
        nonlocal counter
        counter += 1
        return func(*args, **kwargs)

    def print_counter():
        print(f'Counter: {counter}')

    decorated.print_counter = print_counter()

    return decorated

# 在装饰器内包装函数时，保留原始函数的额外属性。而functools模块下的wraps()函数正好可以完成这件事情
def timer(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        pass

    return decorated


#1. 接收参数的装饰器：2 层嵌套
def delayed_start(duration=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator

# 2. 不接收参数的装饰器：1 层嵌套
def delayed_start(func):
    def wrapper(*args, **kwargs):
        ...
    return wrapper

# 8.1.4 用类来实现装饰器（函数替换）
class Foo:
    def __call__(self, name):
        print(f'Hello, {name}')
foo = Foo()
print(callable(foo))
foo('World')

class timer:
    """装饰器：打印函数耗时

    :param print_args: 是否打印方法名和参数，默认为 False
    """

    def __init__(self, print_args):
        self.print_args = print_args

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            st = time.perf_counter()
            ret = func(*args, **kwargs)
            if self.print_args:
                print(f'"{func.__name__}", args: {args}, kwargs: {kwargs}')
            print('time cost: {} seconds'.format(time.perf_counter() - st))
            return ret

        return decorated


# 装饰器模式
class Numbers:
    """一个包含多个数字的简单类"""

    def __init__(self, numbers):
        self.numbers = numbers

    def get(self):
        return self.numbers


class EvenOnlyDecorator:
    """装饰器类：过滤所有偶数"""

    def __init__(self, decorated):
        self.decorated = decorated

    def get(self):
        return [num for num in self.decorated.get() if num % 2 == 0]


class GreaterThanDecorator:
    """装饰器类：过滤大于某个数的数"""

    def __init__(self, decorated, min_value):
        self.decorated = decorated
        self.min_value = min_value

    def get(self):
        return [num for num in self.decorated.get() if num > self.min_value]


obj = Numbers([42, 12, 13, 17, 18, 41, 32])
even_obj = EvenOnlyDecorator(obj)
gt_obj = GreaterThanDecorator(even_obj, min_value=30)
print(gt_obj.get())

"""
（1）基础与技巧· 装饰器最常见的实现方式，是利用闭包原理通过多层嵌套函数实现· 在实现装饰器时，请记得使用wraps()更新包装函数的元数据· 
wraps()不光可以保留元数据，还能保留包装函数的额外属性· 利用仅限关键字参数，可以很方便地实现可选参数的装饰器
（2）使用类来实现装饰器· 只要是可调用的对象，都可以用作装饰器· 实现了__call__方法的类实例可调用· 基于类的装饰器分为两种：
“函数替换”与“实例替换”· “函数替换”装饰器与普通装饰器没什么区别，只是嵌套层级更少· 通过类来实现“实例替换”装饰器，
在管理状态和追加行为上有天然的优势· 混合使用类和函数来实现装饰器，可以灵活满足各种场景
（3）使用wrapt模块· 使用wrapt模块可以方便地让装饰器同时兼容函数和类方法· 使用wrapt模块可以帮你写出结构更扁平的装饰器代码
（4）装饰器设计技巧· 装饰器将包装调用提前到了函数被定义的位置，它的大部分优点也源于此· 
在编写装饰器时，请考虑你的设计是否能很好发挥装饰器的优势· 在某些场景下，类装饰器可以替代元类，并且代码更简单· 
装饰器和装饰器模式截然不同，不要弄混它们· 装饰器里应该只有一层浅浅的包装代码，要把核心逻辑放在其他函数与类中
"""

