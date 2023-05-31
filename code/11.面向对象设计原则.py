import logging
from typing import List, Iterable, Dict
from abc import ABC, abstractmethod
import datetime
"""
SOLID原则剩下的LID如下。
· L：Liskov substitution principle（里式替换原则，LSP）。
· I：interface segregation principle（接口隔离原则，ISP）。
· D：dependency inversion principle（依赖倒置原则，DIP）
LSP是一条用来约束继承的设计原则。继承是一种既强大又危险的技术，LSP为我们提供了很好的指导
ISP与DIP都与面向对象体系里的接口对象有关，前者可以驱动我们设计出更好的接口，后者则会指导我们如何利用接口让代码变得更易扩展。
Python语言不像Java，并没有内置任何接口对象。因此，我的诠释可能会与这两条原则的原始定义略有出入。


（1） LSP· LSP认为子类应该可以任意替代父类使用· 子类不应该抛出父类不认识的异常· 子类方法应该返回与父类一致的类型，或者返回父类返回值的子类型对象
· 子类的方法参数应该和父类方法完全一致，或者要求更为宽松· 某些类可能会存在隐式合约，违反这些合约也会导致违反LSP
（2） DIP· DIP认为高层模块和低层模块都应该依赖于抽象· 编写单元测试有一个原则：测试行为，而不是测试实现· 
单元测试不宜使用太多mock，否则需要调整设计· 依赖抽象的好处是，修改低层模块实现不会影响高层代码· 
在Python中，你可以用abc模块来定义抽象类· 除abc以外，你也可以用Protocol等技术来完成依赖倒置
（3） ISP· ISP认为客户依赖的接口不应该包含任何它不需要的方法· 设计接口就是设计抽象· 写更小的类、更小的接口在大多数情况下是个好主意
"""


# 1. LSP
# 1.避免子类随意抛出异常
# DeactivationNotSupporte异常便显式成为了User类的deactivate()方法协议的一部分。当其他人要编写任何使用User的代码时，都可以针对这个异常进行恰当的处理
class DeactivationNotSupport(Exception):
    """当用户不支持时抛出异常"""


class User:
    def deactivate(self):
        """停用当前用户
        :raises: 当用户不支持停用时，抛出 DeactivationNotSupported 异常 ➊
        """


class Admin(User):
    def deactivate(self):
        raise DeactivationNotSupport('admin can not be deactivated')


def deactivate_users(users: User):
    for user in users:
        try:
            user.deactivate()
        except DeactivationNotSupport:
            logging.info(f"user {user.username} does not aollow deactivating")


# 2.子类随意调整方法参数与返回值
# LSP要求子类方法的返回值类型与父类完全一致，或者返回父类结果类型的子类对象。
# 子类方法可以接收比父类更多的参数，只要保证这些新增参数是可选的
class User:
    def list_related_posts(self):
        pass


class Admin(User):
    def list_related_posts(self, include_hidden: bool = False):
        pass


# 子类与父类参数一致，但子类的参数类型比父类的更抽象
class User:
    def list_related_posts(self, titles=List[str]):
        pass


class Admin(User):
    def list_related_posts(self, titles=Iterable[str]):
        pass


# 2. DIP 依赖倒置原则
# 高层模块不应该依赖低层模块，二者都应该依赖抽象。
# 事实是，抽象的好处显而易见：它解耦了模块间的依赖关系，让代码变得更灵活。
# 但抽象同时也带来了额外的编码与理解成本。所以，了解何时不抽象与何时抽象同样重要。只有对代码中那些容易变化的东西进行抽象，才能获得最大的收益。
class HNWebPage(ABC):
    """抽象类：Hacker News 站点页面"""

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError()


class RemoteHNWebPage(HNWebPage):
    """远程页面，通过请求 Hacker News 站点返回内容"""

    def __init__(self, url: str):
        self.url = url

    def get_text(self) -> str:
        resp = None
        # resp = requests.get(self.url)
        return resp.text


class LocalHNWebPage(HNWebPage):
    """本地页面，根据本地文件返回页面内容

    :param path: 本地文件路径
    """

    def __init__(self, path: str):
        self.path = path

    def get_text(self) -> str:
        with open(self.path, 'r') as fp:
            return fp.read()


class SiteSourceGrouper:
    """对Hacker News 页面的新闻来源站点进行分组统计"""

    def __init__(self, page: HNWebPage):
        self.page = page

    def get_groups(self) -> Dict[str, int]:
        """获取 (域名, 个数) 分组"""
        # html = etree.HTML(self.page.get_text())


def main():
    page = RemoteHNWebPage(url="https://news.ycombinator.com/")
    grouper = SiteSourceGrouper(page).get_groups()


# 3. ISP 接口隔离原则
# 写小类、小接口
class ContentOnlyHNWebPage(ABC):
    """ 抽象类：Hacker News 站点页面（仅提供内容）"""

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError()


class HNWebPage(ABC):
    """ 抽象类：Hacker New 站点页面（含元数据）"""

    @abstractmethod
    def get_text(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_size(self) -> int:
        """ 获取页面大小"""
        raise NotImplementedError()

    @abstractmethod
    def get_generated_at(self) -> datetime.datetime:
        """ 获取页面生成时间"""
        raise NotImplementedError()

