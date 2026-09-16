from langchain.tools import tool

@tool
def add_tool(first:int,second:int) ->str:
    """
    加法运算
    :param first: 第一个数
    :param second: 第二个数
    :return: 两个数的和
    """

    return str(first+second)