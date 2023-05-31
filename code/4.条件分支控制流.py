# 三元表达式
#语法： true_value if <expression> else false_value

# 一个类同时定义了__len__和__bool__两个方法，解释器会优先使用__bool__方法的执行结果。
class UserCollection:
    """用于保存多个用户的集合工具类"""

    def __init__(self, users):
        self.items = users

    def __len__(self):
        return len(self.items)

users = UserCollection(['piglei', 'raymond'])

# 不再需要手动判断对象内部 items 的长度
if users:
    print("There's some users in collection!")

class ScoreJudger:
    """仅当分数大于60 时为真"""

    def __init__(self, score):
        self.score = score

    def __bool__(self):
        return self.score >= 60

# ==运算时行为是可操纵的：只要实现类型的__eq__魔法方法
class EqualWithAnything:
    """与任何对象相等"""

    def __eq__(self, other):
        # 方法里的other 方法代表 == 操作时右边的对象，比如
        # x == y 会调用x 的__eq__方法，other 的参数为 y
        return True
foo = EqualWithAnything()
foo == 'string'

# 令人迷惑的整型驻留技术 对于从-5到256的这些常用小整数，Python会将它们缓存在内存里的一个数组中。
x, y = 6300, 6300
x is y # false
x, y = 100, 100
x is y #true

# bisect(a, x, lo=0, hi=len(a))：在a中查找x，返回x在a中的位置，如果a中存在多个x，则返回任意一个x的位置。如果x不在a中，则返回应该插入x的位置。

# 使用all()/any()函数构建条件表达式
def all_numbers(numbers):
    if not numbers:
        return False
    for n in numbers:
        if n <= 10:
            return False
    return True

def all_numbers1(numbers):
    return bool(numbers) and all(n > 10 for n in numbers)

"""
（1）条件分支语句惯用写法· 不要显式地和布尔值做比较· 利用类型本身的布尔值规则，省略零值判断· 把not代表的否定逻辑移入表达式内部· 
仅在需要判断某个对象是否是None、True、False时，使用is运算符
（2）Python数据模型· 定义__len__和__bool__魔法方法，可以自定义对象的布尔值规则· 定义__eq__方法，可以修改对象在进行==运算时的行为
（3）代码可读性技巧· 不同分支内容易出现重复或类似的代码，把它们抽到分支外可提升代码的可读性· 使用“德摩根定律”可以让有多重否定的表达式变得更容易理解
（4）代码可维护性技巧· 尽可能让三元表达式保持简单· 扁平优于嵌套：使用“提前返回”优化代码里的多层分支嵌套· 当条件表达式变得特别复杂时，可以尝试封装新的函数和方法来简化·
 and的优先级比or高，不要忘记使用括号来让逻辑更清晰· 在使用or运算符替代条件分支时，请注意避开因布尔值运算导致的陷阱
 （5）代码组织技巧· bisect模块可以用来优化范围类分支判断· 字典类型可以用来替代简单的条件分支语句· 尝试总结条件分支代码里的规律，用更精简、更易扩展的方式改写它们·
  使用any()和all()内置函数可以让条件表达式变得更精简
"""