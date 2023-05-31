from typing import List
from abc import ABC, abstractmethod
from urllib import parse
import random
import io
import sys
"""
SOLID 设计原则
· S：single responsibility principle（单一职责原则，SRP）。
· O：open-closed principle（开放–关闭原则，OCP）。
· L：Liskov substitution principle（里式替换原则，LSP）。
· I：interface segregation principle（接口隔离原则，ISP）。
· D：dependency inversion principle（依赖倒置原则，DIP）。


（1） SRP· 一个类只应该有一种被修改的原因· 编写更小的类通常更不容易违反SRP· SRP同样适用于函数，你可以让函数和类协同工作
（2） OCP· 类应该对修改关闭，对扩展开放· 通过分析需求，找到代码中易变的部分，是让类符合OCP的关键· 
使用子类继承的方式可以让类符合OCP· 通过算法类与依赖注入，也可以让类符合OCP· 将数据与逻辑分离，使用数据驱动的方式也是实践OCP的好办法
"""


#  添加类型注解
class Duck:
    def __init__(self, color: str):
        self.color = color

    def quack(self) -> None:
        print(f"I am a {self.color} duck!")


def create_random_ducks(number: int) -> List[Duck]:
    ducks: List[Duck] = []
    for _ in number:
        color = random.choice(['yellow', 'white', 'gray'])
        ducks.append(Duck(color=color))
    return ducks


# 1. SRP单一职责原则 大类拆小类
# 函数同样可以做到单一原则
class Post:
    """ Hacker News 上的条目
    :param title: 标题
    :param link: 链接
    :param points: 当前得分
    :param comments_cnt: 评论数
    """

    def __init__(self, title: str, link: str, points: str, comments_cnt: str):
        self.title = title
        self.link = link
        self.points = int(points)
        self.comments_cnt = int(comments_cnt)


class PostsWriter:
    """负责将帖子列表写入文件中"""

    def __init__(self, fp: io.TextIOBase, title: str):
        self.fp = fp
        self.title = title

    def write(self, posts: List[Post]):
        self.fp.write(f'# {self.title}\n\n')
        for i, post in enumerate(posts, 1):
            self.fp.write(f'> TOP {i}: {post.title}\n')
            self.fp.write(f'> 分数：{post.points} 评论数：{post.comments_cnt}\n')
            self.fp.write(f'> 地址：{post.link}\n')
            self.fp.write('------\n')


class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目"""

    def __init__(self, limit: int = 5):
        pass

    def fetch(self):
        pass


def get_hn_top_posts(fp):
    """获取 Hacker News Top 内容，并将其写入文件中

    :param fp: 需要写入的文件，如未提供，将向标准输出打印
    """
    dest_fp = fp or sys.stdout
    crawler = HNTopPostsSpider()
    writer = PostsWriter(dest_fp, title='Top news on HN')
    writer.write(list(crawler.fetch()))


# 2. OCP 开放–关闭原则
# 类应该对扩展开发，对修改关闭
# 1.通过继承改造代码
class HNTopPostsSpider:
    def fetch(self):
        pass

class GithubOnlyHNTopPostsSpider(HNTopPostsSpider):
    def fetch(self):
        pass

# 2.使用基于组合思想的依赖注入
# 通过抽象与提炼过滤器算法，并结合多态与依赖注入技术，同样让代码符合了OCP。
class PostFilter(ABC):
    """抽象类：定义如何过滤帖子结果"""
    @abstractmethod
    def validate(self, post: Post) -> bool:
        """判断帖子是否应该保留"""
        pass

class DefaultPostFilter(PostFilter):
    """保留所有帖子"""

    def validate(self, post: Post) -> bool:
        return True


class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目

    :param limit: 限制条目数，默认为 5
    :param post_filter: 过滤结果条目的算法，默认保留所有
    """

    items_url = 'https://news.ycombinator.com/'

    def __init__(self, limit: int = 5, post_filter=None):
        self.limit = limit
        self.post_filter = post_filter or DefaultPostFilter()

    def fetch(self):
        # ...
        counter = 0
        post = Post(...)
        # 使用测试方法来判断是否返回该帖子
        if self.post_filter.validate(post):
            counter += 1
            yield post

class GithubPostFilter(PostFilter):
    def validate(self, post: Post) -> bool:
        parsed_link = parse.urlparse(post.link)
        return parsed_link.netloc == 'github.com'

class GithubNBloomPostFilter(PostFilter):
    def validate(self, post: Post) -> bool:
        parsed_link = parse.urlparse(post.link)
        return parsed_link.netloc in ('github.com', 'bloomberg.com')

crawler = HNTopPostsSpider()
crawler = HNTopPostsSpider(post_filter=GithubPostFilter())
crawler = HNTopPostsSpider(post_filter=GithubNBloomPostFilter())


# 3. 数据驱动 将经常变动的部分以数据的方式抽离出来
class HNTopPostsSpider:
    """抓取 Hacker News Top 内容条目
    :param limit: 限制条目数，默认为 5
    :param filter_by_hosts: 过滤结果的站点列表，默认为 None，代表不过滤
    """

    def __init__(self, limit: int = 5, filter_by_hosts=None):
        self.limit = limit
        self.filter_by_hosts = filter_by_hosts

    def fetch(self):
        counter = 0
        post = Post(...)
        # 判断链接是否符合过滤条件
        if self._check_link_from_hosts(post.link):
            counter += 1
            yield post

    def _check_link_from_hosts(self, link: str) -> True:
        """检查某链接是否属于所定义的站点"""
        if self.filter_by_hosts is None:
            return True
        parsed_link = parse.urlparse(link)
        return parsed_link.netloc in self.filter_by_hosts

hosts = None
hosts = ['github.com', 'bloomberg.com']
crawler = HNTopPostsSpider(filter_by_hosts=hosts)