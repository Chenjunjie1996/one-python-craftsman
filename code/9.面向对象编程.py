import random
import os


"""
面向对象有三大基本特征：封装（encapsulation）、继承（inheritance）与多态（polymorphism）
"""


class Duck:
    def __init__(self, color):
        self.color = color

    def quack(self):
        print(f"Hi, I'm a {self.color} duck!")

    """
    虽然类方法通常是用类来调用，但你也可以通过实例来调用类方法，效果一样作为一种特殊方法，类方法最常见的使用场景，
    就是定义工厂方法来生成新实例。类方法的主角是类型本身，当你发现某个行为不属于实例，而是属于整个类型时，可以考虑使用类方法。
    """

    @classmethod
    def create_random(cls):
        color = random.choice(["yellow", "white", "black"])
        return cls(color=color)


d = Duck.create_random()
d.quack()


class Cat:
    def __init__(self, name):
        self.name = name

    def say(self):
        sound = self.get_sound()
        print(f'{self.name}: {sound}...')

    @staticmethod
    def get_sound():
        repeats = random.randrange(1, 10)
        return ' '.join(['Meow'] * repeats)
"""
选择静态方法还是普通函数，可以从以下几点来考虑：
· 如果静态方法特别通用，与类关系不大，那么把它改成普通函数可能会更好；
· 如果静态方法与类关系密切，那么用静态方法更好；
· 相比函数，静态方法有一些先天优势，比如能被子类继承和重写等。
"""

# 属性装饰器
class FilePath:
    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        """获取文件名"""
        return self.path.rsplit(os.sep, 1)[-1]
    @basename.setter
    def basename(self, name):
        """修改当前路径里的文件名部分"""
        new_path = self.path.rsplit(os.sep, 1)[:-1] + [name]
        self.path = os.sep.join(new_path)
    @basename.deleter
    def basename(self):
        raise RuntimeError('Can not delete basename!')
p = FilePath('/tmp/foo.py')
p.basename = 'bar.txt'
print(p.path)
# del p.basename

# 鸭子类型是一种编程风格 鸭子类型只关心行为，不关心类型


"""
 Mixin 模式
 Mixin是一种把额外功能“混入”某个类的技术。
 Mixin类通常很简单，只实现一两个功能，所以很多时候为了实现某个复杂功能，一个类常常会同时混入多个Mixin类
"""

class InfoDumperMixin:
    """Mixin：输出当前实例信息"""
    def dump_info(self):
        d = self.__dict__
        print("Number of members: {}".format(len(d)))
        print("Details:")
        for key, value in d.items():
            print(f' - {key}: {value}')

class Person(InfoDumperMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age



"""
（1）语言基础知识· 类与实例的数据，都保存在一个名为__dict__的字典属性中· 灵活利用__dict__属性，能帮你做到常规做法难以完成的一些事情· 
使用@classmethod可以定义类方法，类方法常用作工厂方法· 使用@staticmethod可以定义静态方法，静态方法不依赖实例状态，是一种无状态方法· 
使用@property可以定义动态属性对象，该属性对象的获取、设置和删除行为都支持自定义
（2）面向对象高级特性· Python使用MRO算法来确定多重继承时的方法优先级· super()函数获取的并不是当前类的父类，而是当前MRO链条里的下一个类· 
Mixin是一种基于多重继承的有效编程模式，用好Mixin需要精心的设计· 元类的功能相当强大，但同时也相当复杂，除非开发一些框架类工具，否则你极少需要使用元类· 
元类有许多更简单的替代品，比如类装饰器、子类化钩子方法等· 通过定义__init_subclass__钩子方法，你可以在某个类被继承时执行自定义逻辑
（3）鸭子类型与抽象类· 鸭鸭“鸭子类型”是Python语言最为鲜明的特点之一，在该风格下，一般不做任何严格的类型检查· 虽然“鸭子类型”非常实用，
但是它有两个明显的缺点——缺乏标准和过于隐式· 抽象类提供了一种更灵活的子类化机制，我们可以通过定义抽象类来改变isinstance()的行为· 
通过@abstractmethod装饰器，你可以要求抽象类的子类必须实现某个方法
（4）面向对象设计· 继承提供了相当强大的代码复用机制，但同时也带来了非常紧密的耦合关系· 错误使用继承容易导致代码失控· 对事物的行为而不是事物本身建模，
更容易孵化出好的面向对象设计· 在创建继承关系时应当谨慎。用组合来替代继承有时是更好的做法
（5）函数与面向对象的配合· Python里的面向对象不必特别纯粹，假如用函数打一点儿配合，你可以设计出更好的代码· 可以像requests模块一样，
用函数为自己的面向对象模块实现一些更易用的API· 在Python中，我们极少会应用真正的“单例模式”，大多数情况下，一个简单的模块级全局对象就够了· 
使用“预绑定方法模式”，你可以快速为普通实例包装出类似普通函数的API
（6）代码编写细节· Python的成员私有协议并不严格，如果你想标示某个属性为私有，使用单下划线前缀就够了· 
编写类时，类方法排序应该遵循某种特殊规则，把读者最关心的内容摆在最前面· 多态是面向对象编程里的基本概念，同时也是最强大的思维工具之一· 
多态可能的介入时机：许多类似的条件分支判断、许多针对类型的isinstance()判断


"""



