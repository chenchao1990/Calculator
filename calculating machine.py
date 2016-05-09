#!/usr/bin/env python
# _*_coding:utf-8 _*_

import re


def process_mul_div(arg):
    '''处理乘除'''

    val = arg[0]  #匹配带乘除的表达式 如果没有，直接结束处理
    ret = re.search('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*',val)
    if not ret:
        return
    content = re.search('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*',val).group()
                        #40.0/5
    if len(content.split('*')) > 1:
        n1,n2 = content.split('*')
        value = float(n1) * float(n2)
    else:
        n1,n2 = content.split('/')
        value = float(n1) / float(n2)

    before,after = re.split('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*',val,1)
    new_str = "%s%s%s" % (before,value,after)
    arg[0] = new_str
    process_mul_div(arg)


def process_plus_minus(arg):

    while True:
        if arg[0].__contains__('+-') or arg[0].__contains__('++') or arg[0].__contains__('-+') or arg[0].__contains__('--'):
            arg[0] = arg[0].replace('+-','-')
            arg[0] = arg[0].replace('++','+')
            arg[0] = arg[0].replace('-+','-')
            arg[0] = arg[0].replace('--','+')
        else:
            break
        #此时表打死里面没有双重号，+12.0-81+41

    if arg[0].startswith('-'):
        arg[1] +=1
        arg[0] = arg[0].replace('-','&')
        arg[0] = arg[0].replace('+','-')
        arg[0] = arg[0].replace('&','+')
        arg[0] = arg[0][1:]

    val = arg[0]       #12.1-15.6
    mch = re.search('\d+\.*\d*[\+\-]{1}\d+\.*\d*', val)

    #如果表达式里没有加减运算，直接返回结束处理

    if not mch:
        return
    #如果表达式里还有加减运算，继续处理
    content = re.search('\d+\.*\d*[\+\-]{1}\d+\.*\d*', val).group()

    if len(content.split('+')) > 1:
        n1,n2 = content.split('+')
        value = float(n1) + float(n2)

    else:
        n1,n2 = content.split('-')
        value = float(n1) - float(n2)

    #原列表中表达式经过去双重+—号后 为+12.0-81+41，将此分割

    before,after = re.split('\d+\.*\d*[\+\-]{1}\d+\.*\d*',val,1)
    new_str = "%s%s%s" % (before,value,after)
    arg[0] = new_str

    process_plus_minus(arg)


def compute(expression):

    inp = [expression,0]

    #先处理乘除
    process_mul_div(inp)

    #在处理加减
    process_plus_minus(inp)

    if divmod(inp[1],2)[1] ==1:
        result = float(inp[0])
        result = result * -1
    else:
        result = float(inp[0])

    return  result


def process_bracket(expression):
    #inpp = '1-2*((60-30+(-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
    # 没有括号


    if not re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)',expression):
        fin = compute(expression)
        return  fin

    else:           # 有括号的时候
        a_layer_bracket = re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)',expression).group()
        in_bracket = a_layer_bracket[1:len(a_layer_bracket)-1]
        ret = compute(in_bracket)  #将匹配到的单层括号计算出结果
        #将原表达式分割成三部分
        before,nothing,after = re.split('\(([\+\-\*\/]*\d+\.*\d*){2,}\)',expression,1)
        new_express = "%s%s%s" % (before,ret,after)
        return  process_bracket(new_express)


if __name__ == '__main__':

    inpp = '1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) ) '
    new_inpp = re.sub("\s*",'',inpp)
    print new_inpp
    result = process_bracket(new_inpp)

    print result



