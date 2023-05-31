# 最常见的内置容器类型有四种：列表、元组、字典、集合。

# 元组存放结构化数据
user_info = ('piglei', 'MALE', 30, True)
print(user_info[2])

# 具名元组 能通过名称而不止数组索引来访问
from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'width,height')
rect = Rectangle(width=100, height=20)
print(rect[0])
print(rect.width)

# 字典 python3.7后 字典有序
# 使用setdefault取值并修改
d = {'title': 'foobar'}
d.setdefault('items', []).append('foo')
print(d)
d.setdefault('items', []).append('bar')
print(d)
# 使用pop方法删除不存在的键
d.pop('is', None)  # 在键不存在的情况下也不会产生任何异常
d.pop('items', None)
print(d)

# 浅拷贝与深拷贝
nums = [1, 2, 3]
nums.copy()
nums[:]
[i for i in nums]
# 大部分情况下，浅拷贝操作足以满足我们对可变类型的复制需求。但对于一些层层嵌套的复杂数据来说，浅拷贝仍然无法解决嵌套对象被修改的问题。
items = [1, ['foo', 'bar'], 2, 3]

# 枚举类型
from enum import Enum

class PagePerfLevel(str, Enum):
    LT_100 = 'less than 100ms'
    LT_300 = 'between 100ms and 300ms'
    LT_1000 = 'between 300ms and 1s'
    GT_1000 = 'greater than 1000ms'

# 继承
from collections.abc import MutableMapping
from collections import defaultdict

class PerfLevelDict(MutableMapping):
    class PerfLevelDict(MutableMapping):
        """存储响应时间性能等级的字典"""

        def __init__(self):
            self.data = defaultdict(int)

        def __getitem__(self, key):
            """当某个性能等级不存在时，默认返回 0"""
            return self.data[self.compute_level(key)]

        def __setitem__(self, key, value):
            """将 key 转换为对应的性能等级，然后设置值"""
            self.data[self.compute_level(key)] = value

        def __delitem__(self, key):
            del self.data[key]

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

        def items(self):
            """按照顺序返回性能等级数据"""
            return sorted(
                self.data.items(),
                key=lambda pair: list(PagePerfLevel).index(pair[0]),
            )

        def total_requests(self):
            """返回总请求数"""
            return sum(self.values())

# 生成器
def generate_even(max_number):
    """一个简单生成器，返回 0 到 max_number 之间的所有偶数"""
    for i in range(0, max_number):
        if i % 2 == 0:
            yield i
for i in generate_even(10):
    print(i)
i = generate_even(10)
print(f"{next(i)}, {next(i)}")

# 避开列表的性能陷阱
# 列表头部插入数据
from collections import deque
l = deque()
for i in range(5000):
    l.appendleft(i)
# 判断成员是否存在，用集合操作

# 快速合并字典 **解包字典 *解包可迭代对象
d1 = {'name': 'apple'}
d2 = {'price': 10}
print({**d1, **d2})

l1 = [1, 2]
l2 = [3, 4]
print([*l1, *l2])

# 有序字典去重
from collections import OrderedDict
nums = [10, 2, 3, 21, 10, 3]
set(nums)
print(OrderedDict.fromkeys(nums))
order_rmdup = list(OrderedDict.fromkeys(nums).keys())
print(order_rmdup)

# 别在遍历列表时同步修改

# 让函数返回NamedTuple
from typing import NamedTuple

class Address(NamedTuple):
    country: str
    province: str
    city: str

def latlon_to_address(lat, lon):
    country = 1
    province = 2
    city = 3
    return Address(
        country=country,
        province=province,
        city=city,
    )

"""
（1）基础知识· 在进行函数调用时，传递的不是变量的值或者引用，而是变量所指对象的引用· Python内置类型分为可变与不可变两种，可变性会影响一些操作的行为，比如+=· 
对于可变类型，必要时对其进行拷贝操作，能避免产生意料之外的影响· 常见的浅拷贝方式：copy.copy、推导式、切片操作· 使用copy.deepcopy可以进行深拷贝操作
（2）列表与元组· 使用enumerate可以在遍历列表的同时获取下标· 函数的多返回值其实是一个元组· 不存在元组推导式，但可以使用tuple来将生成器表达式转换为元组· 
元组经常用来表示一些结构化的数据
（3）字典与集合· 在Python 3.7版本前，字典类型是无序的，之后变为保留数据的插入顺序· 使用OrderedDict可以在Python 3.7以前的版本里获得有序字典· 
只有可哈希的对象才能存入集合，或者作为字典的键使用· 使用有序字典OrderedDict可以快速实现有序去重· 
使用fronzenset可以获得一个不可变的集合对象· 集合可以方便地进行集合运算，计算交集、并集· 不要通过继承dict来创建自定义字典类型
（4）代码可读性技巧· 具名元组比普通元组可读性更强· 列表推导式可以更快速地完成遍历、过滤、处理以及构建新列表操作· 不要编写过于复杂的推导式，用朴实的代码替代就好· 
不要把推导式当作代码量更少的循环，写普通循环就好
（5）代码可维护性技巧· 当访问的字典键不存在时，可以选择捕获异常或先做判断，优先推荐捕获异常· 使用get、setdefault、带参数的pop方法可以简化边界处理逻辑· 
使用具名元组作为返回值，比普通元组更好扩展· 当字典键不存在时，使用defaultdict可以简化处理· 
继承MutableMapping可以方便地创建自定义字典类，封装处理逻辑· 用生成器按需返回成员，比直接返回一个结果列表更灵活，也更省内存· 
使用动态解包语法可以方便地合并字典· 不要在遍历列表的同时修改，否则会出现不可预期的结果
（6）代码性能要点· 列表的底层实现决定了它的头部操作很慢，deque类型则没有这个问题· 当需要判断某个成员在容器中是否存在时，使用字典/集合更快
"""



