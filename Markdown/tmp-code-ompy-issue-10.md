# Markdown 列表FAQ(FAQ about Markdown List) #

## Q1 重新计数 与 缩进 ##

### 表现 ###

1. 水果

苹果  
李子

2. 蔬菜

生菜  
西红柿

3. 肉类

鸡肉  
鱼肉

### 概述 ###

这里的问题是：

1. **每个列表都重新计数了（从 1 开始）**
2. 每个列表下面的具体内容看起来并没有归该表头所有（没有缩进）


### 分析 ###

造成问题的原始代码如下：

> `1. 水果`  
> 
> `苹果`
> `李子`
> 
> `2. 蔬菜`  
> 
> `生菜`
> `西红柿`
> 
> `3. 肉类`  
> 
> `鸡肉`
> `鱼肉`


注意到：每个列表内容**前后均有一个空行**。  

### 尝试1 ###

让我们删去表头与其**下**内容之间的空行试试，即当代码是这样的时候：
> `1. 水果` 
> `苹果`
> `李子`
> 
> `2. 蔬菜`
> `生菜`
> `西红柿`
> 
> `3. 肉类`
> `鸡肉`
> `鱼肉`

显示效果是： 

1. 水果  
苹果
李子

2. 蔬菜  
生菜
西红柿

3. 肉类  
鸡肉
鱼肉

两个问题都得到了解决！  

### 尝试2 ###

要是删去表头与其**上**内容之间的空行，即当代码是这样的时候：
> `1. 水果`
> 
> `苹果`
> `李子`
> `2. 蔬菜`
> 
> `生菜`
> `西红柿`
> `3. 肉类`
> 
> `鸡肉`
> `鱼肉`

显示效果是：

1. 水果

苹果
李子
2. 蔬菜
 
生菜
西红柿
3. 肉类
 
鸡肉
鱼肉

看来这 2 个问题都没有得到解决（注意到 2 和 3 被 markdown 的实现当成了文本来处理）。

### 尝试3 ###

要是将这两个空行都删除，即当代码是这样的时候：
> `1. 水果`
> `苹果`
> `李子`
> `2. 蔬菜`
> `生菜`
> `西红柿`
> `3. 肉类`
> `鸡肉`
> `鱼肉`

显示效果是：  

1. 水果  
苹果  
李子
2. 蔬菜  
生菜  
西红柿
3. 肉类  
鸡肉  
鱼肉

在 GitHub 下的实现好像也可以？
在 MarkdownPad 2 下的实现是和尝试2结果一致的，均被编辑器当成文本，而不会被当成列表。

### A1 解决 ###

综上所述：

1. 为了避免列表出现上述**重新计数**问题，写列表时请**直接将项目内容直接紧跟在其表头后**，而不要在表头与其统辖的项目内容之间加入空行。
2. 就目前的实验结果看来，在 Markdown 的 GitHub 实现中，只要代码符合第 1 点，就不会出现列表缩进问题；而在 MarkdownPad 2 实现中，为了避免出现上述的列表下缩进问题，请在第 n 个列表项目内容尾部、第 n+1 个列表项目序号之间加入一个空行。


## Q2 列表与正文粘在一起 ##

### 表现 ###

比如说我本想在这段话后跟上一个列表，却出现这种状况：
1. 列表1
2. 列表2
3. 列表3

### 概述 ###

这里的问题是：

1. 列表与正文粘在一起了，没有与正文独立开来


### 分析 ###

造成问题的原始代码如下：

`比如说我本想在这段话后跟上一个列表，却出现这种状况：` 
`1. 列表1`
`2. 列表2`
`3. 列表3`

注意到原始代码中列表与正文之间**只有一个换行符**

### 尝试1 ###

考虑到[《如何在 markdown 语法下键入换行符》](https://github.com/OpenMindClub/OMOOC.py/issues/9)一文中提到了：


> 写作者必须键入**2个连续的**`空格`之后再按`Enter`，才能完成`强制换行`这个动作
 
那么在正文与列表之间加入两个连续的空格是看看，即当代码是这样的时候（1个[Space]表示此处有1个空格）：

`比如说我本想在这段话后跟上一个列表，却出现这种状况：[Space][Space]`
`1. 列表1`
`2. 列表2`
`3. 列表3`  

显示效果是：  

比如说我本想在这段话后跟上一个列表，却出现这种状况：  
1. 列表1
2. 列表2
3. 列表3

看来问题没有得到实质性的解决：markdown 没有把代码识别为列表，而是认为这串代码是正文。

### 尝试2 ###

显然不能考虑在每个列表的表头后插入两个空格，因为这样仅仅是将代码视为正文来处理，没有解决实质性问题。  
那么我们不妨在列表最前面与正文之间再插入一个空行，即当代码是这样的时候（[Newline]表示此处键入 1 个换行符，即1个`Enter`）：

`比如说我本想在这段话后跟上一个列表，却出现这种状况：` 
`[Newline]`
`1. 列表1`
`2. 列表2`
`3. 列表3`

显示效果是：  

比如说我本想在这段话后跟上一个列表，却出现这种状况：  

1. 列表1
2. 列表2
3. 列表3

问题好像得到解决了？再向表头下面添加项目试试看：

比如说我本想在这段话后跟上一个列表，却出现这种状况：  

1. 列表1
 1. 项目1.1
 2. 项目1.2
2. 列表2
 1. 项目2.1
 2. 项目2.2
3. 列表3
 1. 项目3.1
 2. 项目3.2

非常好，问题得到了圆满解决。

### A2 解决 ###

综上所述：
为了让 markdown 能识别出列表，应在正文与列表之间插入一个空行，亦即两个换行符（键入2个`Enter`）。