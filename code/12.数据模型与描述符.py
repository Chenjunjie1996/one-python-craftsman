"""
1）字符串相关协议· 使用__str__方法，可以定义对象的字符串值（被str()触发）· 使用__repr__方法，可以定义对象对调试友好的详细字符串值（被repr()触发）
· 如果对象只定义了__repr__方法，它同时会用于替代__str__· 使用__format__方法，可以在对象被用于字符串模板渲染时，提供多种字符串值（被.format()触发）
（2）比较运算符重载· 通过重载与比较运算符有关的6个魔法方法，你可以让对象支持==、>=等比较运算·
使用functools.total_ordering可以极大地减少重载比较运算符的工作量
（3）描述符协议· 使用描述符协议，你可以轻松实现可复用的属性对象· 实现了__get__、__set__、__delete__其中任何一个方法的类都是描述符类
· 要在描述符里保存实例级别的数据，你需要将其存放在instance.dict里，而不是直接放在描述符对象上
4）数据类与自定义哈希运算· 要让自定义类支持集合运算，你需要实现__eq__与__hash__两个方法
· 如果两个对象相等，它们的哈希值也必须相等，否则会破坏哈希表的正确性· 不同对象的哈希值可以一样，哈希冲突并不会破坏程序正确性，但会影响效率
· 使用dataclasses模块，你可以快速创建一个支持哈希操作的数据类· 要让数据类支持哈希操作，你必须指定frozen=True参数将其声明为不可变类型
· 一个对象的哈希值必须在它的生命周期里保持不变
（5）其他建议· 虽然数据模型能帮我们写出更Pythonic的代码，但切勿过度推崇
· __del__方法不是在执行del语句时被触发，而是在对象被作为垃圾回收时被触发· 不要使用__del__来做任何“自动化”的资源回收工作
"""

from functools import total_ordering

class Person:
    def __init__(self, name, age, favorite_color):
        self.name = name
        self.age = age
        self.favorite_color = favorite_color

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{cls_name}(name={name!r}, age={age!r}, favorite_color={color!r})".format(
            cls_name=self.__class__.__name__,
            name=self.name,
            age=self.age,
            color=self.favorite_color,
        )

    def __format__(self, format_spec):
        if format_spec == "verbose":
            return f"{self.name}({self.age})[{self.favorite_color}]"
        elif format_spec == "simple":
            return f"{self.name}({self.age})"
        return self.name


p = Person("piglei", 18, "black")
print(p)
print(repr(p))
# 假如一个类型没定义__str__方法，只定义了__repr__，那么__repr__的结果会用于所有需要字符串的场景。


class Square:
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length ** 2

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.length == other.length
        return False

    def __ne__(self, other):
        return not self.length == other.length

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.length < other.length
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.length > other.length
        return NotImplemented

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


"""
如果使用@total_ordering装饰一个类，那么在重载类的比较运算符时，
你只要先实现__eq__方法，然后在__lt__、__le__、__gt__、__ge__四个方法里随意挑一个实现即可，@total_ordering会帮你自动补全剩下的所有方法。
"""
@total_ordering
class Square:
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length ** 2

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.length == other.length
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.length < other.length
        return NotImplemented


# 描述符
# 使用@property把age定义为property对象后，我可以很方便地增加校验逻辑
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("value is not valid integer")
        if not (0 < value < 150):
            raise ValueError("value must between 0 and 150")
        self._age = value


# 描述符（descriptor）是Python对象模型里的一种特殊协议，它主要和4个魔法方法有关：__get__、__set__、__delete__和__set_name__。
class InfoDescriptor:
    """打印帮助信息的描述符"""
    def __get__(self, instance, owner=None):
        print(f'Calling __get__, instance: {instance}, owner: {owner}')
        if not instance:
            print('Calling without instance...')
            return self
        return 'informative descriptor'

    def __set__(self, instance, value):
        print(f'Calling __set__, instance: {instance}, value: {value}')

    def __delete__(self, instance):
        raise RuntimeError("Deletion not supported")


# 描述符的__get__方法，会在访问owner类或owner类实例的对应属性时被触发。__get__方法里的两个参数的含义如下。
# · owner：描述符对象所绑定的类。· instance：假如用实例来访问描述符属性，该参数值为实例对象；如果通过类来访问，该值为None。
class Foo:
    bar = InfoDescriptor()


Foo.bar
Foo().bar
f = Foo()
f.bar = 42
# del f.bar


# 用描述符实现属性校验功能
class IntegerField:
    """整型字段，只允许一定范围内的整型值
    :param min_value: 允许的最小值
    :param max_value: 允许的最大值
    """
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance, owner=None):
        # 当不是通过实例访问，直接返回描述对象
        if not instance:
            return self
        # 返回保存在实例字典里的值
        return instance.__dict__["_integer_field"]

    def __set__(self, instance, value):
        # 检验后将值保存在字典里
        value = self._validate_value(value)
        instance.__dict__["_integer_field"] = value

    def _validate_value(self, value):
        """检验值是否为符合要求的整数"""
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError('value is not a valid integer!')
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f'value must between {self.min_value} and {self.max_value}!'
            )
        return value

    """使用__set_name__方法，不同字段间不会互相影响
    · owner：描述符对象当前绑定的类。
    · name：描述符所绑定的属性名称。
    """
    def __set_name__(self, owner, name):
        # 将绑定属性名保存在描述符对象中
        # 对于age=IntegerField()来说，此处的name就是age
        self._name = name


class Person:
    age = IntegerField(min_value=0, max_value=150)

    def __init__(self, name, age):
        self.name = name
        self.age = age


class Rectangle:
    width = IntegerField(min_value=1, max_value=10)
    height = IntegerField(min_value=1, max_value=5)


class DuckWithProperty:
    """
    property是数据描述符，你无法直接通过重写修改
    """
    @property
    def color(self):
        return "grey"


#去过普吉岛的人员数据
users_visited_phuket = [
    {
        "first_name": "Sirena",
        "last_name": "Gross",
        "phone_number": "650-568-0388",
        "date_visited": "2018-03-14",
    },
]

# 去过新西兰的人员数据
users_visited_nz = [
    {
        "first_name": "Justin",
        "last_name": "Malcom",
        "phone_number": "267-282-1964",
        "date_visited": "2011-03-13",
    },

    {
        "first_name": "Sirena",
        "last_name": "Gross",
        "phone_number": "650-568-0388",
        "date_visited": "2018-03-14",
    },
]

class VisitRecord:
    """旅客记录"""
    def __init__(self, first_name, last_name, phone_number, date_visited):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_visited = date_visited

    def __hash__(self):
        return hash(self.comparable_fields)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.comparable_fields == other.comparable_fields
        return False

    @property
    def comparable_fields(self):
        """ 获取用于比较对象的字符串 """
        return (self.first_name, self.last_name, self.phone_number)

def find_potential_customers():
    return set(VisitRecord(**r) for r in users_visited_phuket) - set(VisitRecord(**r) for  r in users_visited_nz)


from dataclasses import dataclass, field
# frozen=True 显示将当前类变成不可变类型
@dataclass(frozen=True)
class VisitRecordDC:
    first_name: str
    last_name: str
    phone_number: str
    date_visited: str = field(compare=False)

print(set(VisitRecord(**r).first_name for  r in users_visited_nz))
print(set(VisitRecord(**r).last_name for  r in users_visited_nz))
print((set(VisitRecord(**r).phone_number for  r in users_visited_nz)))
print((set(VisitRecord(**r).date_visited for  r in users_visited_nz)))