from typing import List


def remove_invalid(items: List[int]):
    """剔除无效元素"""
    pass


"""
描述性弱的名字：看不懂在做什么
value = process(s.strip())
描述性强的名字：尝试从用户输入里解析出一个用户名
username = extract_username(input_string.strip())

计算机科学领域只有两件难事：缓存失效和命名

能不定义变量就别定义

Python之禅：显式优于隐式

先写注释，后写代码
"""

# 不要有太多变量，对局部变量分组建模
class ImportedSummary:
    """保存导入结果摘要的数据类"""

    def __init__(self):
        self.succeeded_count = 0
        self.failed_count = 0

class ImportingUserGroup:
    """用于暂存用户导入处理的数据类"""

    def __init__(self):
        self.duplicated = []
        self.banned = []
        self.normal = []


def parse_user(line):
    pass


def import_users_from_file(fp):
    """尝试从文件对象读取用户，然后导入数据库　　

    :param fp: 可读文件对象
    :return: 成功与失败的数量
    """
    importing_user_group = ImportingUserGroup()
    for line in fp:
        parsed_user = parse_user(line)
        # …… 进行判断处理，修改上面定义的importing_user_group 变量

    summary = ImportedSummary()
    # …… 读取 importing_user_group，写入数据库并修改成功与失败的数量

    return summary.succeeded_count, summary.failed_count


""" Summarize
（1）变量和注释决定“第一印象”· 变量和注释是代码里最接近自然语言的东西，它们的可读性非常重要· 即使是实现同一个算法，变量和注释不一样，给人的感觉也会截然不同
（2）基础知识· Python的变量赋值语法非常灵活，可以使用*variables星号表达式灵活赋值· 编写注释的两个要点：不要用来屏蔽代码，而是用来解释“为什么”· 
接口注释是为使用者而写，因此应该简明扼要地描述函数职责，而不必包含太多内部细节· 可以用Sphinx格式文档或类型注解给变量标明类型
（3）变量名字很重要· 给变量起名要遵循PEP 8原则，代码的其他部分也同样如此· 尽量给变量起描述性强的名字，但评价描述性也需要结合场景· 
在保证描述性的前提下，变量名要尽量短· 变量名要匹配它所表达的类型· 可以使用一两个字母的超短名字，但注意不要过度使用
（4）代码组织技巧· 按照代码的职责来组织代码：让变量定义靠近使用· 适当定义临时变量可以提升代码的可读性· 不必要的变量会让代码显得冗长、啰唆· 
同一个作用域内不要有太多变量，解决办法：提炼数据类、拆分函数· 空行也是一种特殊的“注释”，适当的空行可以让代码更易读
（5）代码可维护性技巧· 保持变量在两个方面的一致性：名字一致性与类型一致性· 显式优于隐式：不要使用locals()批量获取变量· 
把接口注释当成一种函数设计工具：先写注释，后写代码
"""

