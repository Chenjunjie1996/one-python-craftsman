# 布尔值可作为整型使用
numbers = [1, 2, 4, 5, 7]
count = sum(i % 2 == 0 for i in numbers)

# s.partition() / s.translate()
s = "name:piglei"
print(s.partition(':'))
print(s.partition(';'))

# 按规则一次性替换多个字符，使用它比调用多次replace方法更快也更简单：
s = '明明是中文,却使用了英文标点.'
# 创建替换规则表：',' -> '，', '.' -> '。'
table = s.maketrans(',.', '，。')
s = s.translate(table)
print(s)

# 字符串与字节串
"""
（1）字符串：我们最常挂在嘴边的“普通字符串”，有时也被称为文本（text），是给人看的，对应Python中的字符串（str）类型。
str使用Unicode标准，可通过.encode()方法编码为字节串。
（2）字节串：有时也称“二进制字符串”（binary string），是给计算机看的，对应Python中的字节串（bytes）类型。
bytes一定包含某种真正的字符串编码格式（默认为UTF-8），可通过.decode()解码为字符串。
"""

# 使用Jinja2模板处理字符串
from jinja2 import Template
_MOVIES_TMPL = '''\
Welcome, {{username}}.
{%for name, rating in movies %}
* {{ name }}, Rating: {{ rating|default("[NOT RATED]", True) }}
{%- endfor %}
'''
def render_movies_j2(username, movies):
    tmpl = Template(_MOVIES_TMPL)
    return tmpl.render(username=username, movies=movies)

# dedent方法会删除整段字符串左侧的空白缩进
from textwrap import dedent
message = dedent("""\
            Welcome, today's movie list:
            - Jaw (1975)
            - The Shining (1980)
            - Saw (2004)""")

"""
（1）数值基础知识· Python的浮点数有精度问题，请使用Decimal对象做精确的小数运算· 布尔类型是整型的子类型，布尔值可以当作0和1来使用· 使用float('inf')无穷大可以简化边界处理逻辑
（2）字符串基础知识· 字符串分为两类：str（给人阅读的文本类型）和bytes（给计算机阅读的二进制类型）· 通过.encode()与.decode()可以在两种字符串之间做转换· 优先推荐的字符串格式化方式（从前往后）：
f-string、str.format()、C语言风格格式化· 使用以r开头的字符串内置方法可以从右往左处理字符串，特定场景下可以派上用场· 字符串拼接并不慢，不要因为性能原因害怕使用它
（3）代码可读性技巧· 在定义数值字面量时，可以通过插入_字符来提升可读性· 不要出现“神奇”的字面量，使用常量或者枚举类型替换它们· 
保留数学算式表达式不会影响性能，并且可以提升可读性· 使用textwrap.dedent()可以让多行字符串更好地融入代码
（4）代码可维护性技巧· 当操作SQL语句等结构化字符串时，使用专有模块比裸处理的代码更易于维护· 使用Jinja2模板来替代字符串拼接操作
（5）语言内部知识· 使用dis模块可以查看Python字节码，帮助我们理解内部原理· 使用timeit模块可以对Python代码方便地进行性能测试· Python语言进化得很快，不要轻易被旧版本的“经验”所左右
"""
