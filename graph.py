import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk


root = tk.Tk()  # 创建底层窗口，每个程序中只能存在一个，并应在其他组件前创建
root.title("判断序列是否可图小应用")
root.geometry('400x300')   # root窗口大小


# 定义输入框和按钮
input_label = tk.Label(root, text="请输入一个有限非负整数序列，用空格分隔：",font=('newspaper', 12),width = 40,height = 10)   # 创建一个Label组件
input_label.pack(side = tk.TOP)   # 将组件可视化
input_entry = tk.Entry(master=root,width = 50)      # 生成文本框
input_entry.pack()

# 设置tk文字存储器
var = tk.StringVar()
# 文字变量储存器
l = tk.Label(root,
             textvariable=var,
             # 使用 textvariable可以变化,text的变量
             bg='green',
             # 背景颜色
             font=('newspaper', 12),
             # 字体和字体大小
             width=15,
             height=2
             ##标签长宽
             )
l.pack()



"""
    return 1 不满足握手定理  0 满足
"""
def checkodd(sequence):
    count = 0
    for i in range(len(sequence)):
        count += sequence[i]
    return count % 2

def get_key(val,dict):
    for key, value in dict.items():
         if val == value:
             return key

"""
    得到简单图的邻接矩阵
"""
def Get_Matrix(d_dict,matrix_d):
    # 模拟栈
    stack = []
    # j = 0
    support_flag = True
    matrix_d = matrix_d

    """
        每一次循环是执行了一步----将序列进行迭代
        当下一次的迭代 序列全部变为0 or 序列中出现-1 就停止迭代
    """
    while ((np.array(list(d_dict.values())) < 0).any() == False) & (
            (np.array(list(d_dict.values())) == 0).all() == False):
        # j = j + 1
        # print("第", j, "次迭代....")
        # 将满足要求的序列压入栈
        stack.append(d_dict)

        # 当序列不满足握手定理，中断迭代，并且将标志位 support_flag 置为False
        if (checkodd(list(d_dict.values())) == 1):
            support_flag = False
            break

        # 对字典内的元素按照健进行正序（当前度序列的大小进行正序）
        d_dict = {k: v for k, v in sorted(d_dict.items(), key=lambda item: item[1], reverse=True)}

        # 创建后续用于序列迭代的字典
        d_dict_next = d_dict.fromkeys(d_dict, 0)
        # 将排序后的第一个元素删除
        d_dict_next.pop(list(d_dict.keys())[0])

        # 将序列的d1取出，后面的度进行减一操作，直到 d_(d1+1) 为止
        # d_dict = (d1,d2,d3,d4,d5,...,dn) ,  n-1 >= d1>=d2>=d3>=d4>=d5>=....>=dn
        # d_dict_next = (d2-1,d3-1,d4-1,d5-1,...,d(d1+1)-1,d(d1+2),...,dn)
        flag = d_dict[list(d_dict.keys())[0]]
        for i in range(len(d_dict_next)):
            if (i <= flag - 1):
                d_dict_next[list(d_dict_next.keys())[i]] = d_dict[list(d_dict.keys())[i + 1]] - 1
            else:
                d_dict_next[list(d_dict_next.keys())[i]] = d_dict[list(d_dict.keys())[i + 1]]
        print(d_dict_next)
        # 将d_dict_next 赋值给 d_dict用于下一步迭代
        d_dict = d_dict_next

    """
        当上面迭代的度序列均满足握手定理
        则将压入栈的度序列，进行回溯，从而对邻接矩阵进行更新
    """
    if support_flag ==  True:
        # 输入的序列不全部为0
        if len(stack) != 0 :
            # 回溯更新邻接矩阵(首次更新)
            stack_top = stack.pop()
            max_num = 0
            mid_dict = {}
            for ele in stack_top.values():
                if ele >= max_num:
                    max_num = ele

            if (max_num != 1):
                v_max = get_key(max_num, stack_top)
                max_order = int(v_max.split('_')[1])
                # 将最大度的点于其他度为1的点进行链接
                list_of_key = list(stack_top.keys())
                list_of_value = list(stack_top.values())
                for i in range(len(list_of_value)):
                    if list_of_value[i] == 1:
                        mid_dict[list_of_key[i]] = list_of_value[i]
                for j in range(max_num):
                    rand_key_value = mid_dict.popitem()
                    rand_key = rand_key_value[0]
                    rand_key_order = int(rand_key.split('_')[1])
                    # 邻接矩阵更新
                    matrix_d[max_order - 1][rand_key_order - 1] += 1
                    matrix_d[rand_key_order - 1][max_order - 1] += 1

                # 如果此时 mid_dcit 中还剩下 元素 则全为1 且 为偶数
                for k in range(int(len(mid_dict) / 2)):
                    the_one_key_value = mid_dict.popitem()
                    the_one_key = the_one_key_value[0]
                    the_one_order = int(the_one_key.split('_')[1])

                    the_second_key_value = mid_dict.popitem()
                    the_second_key = the_second_key_value[0]
                    the_second_order = int(the_second_key.split('_')[1])
                    matrix_d[the_one_order - 1][the_second_order - 1] += 1
                    matrix_d[the_second_order - 1][the_one_order - 1] += 1

            #  stack_top 全部为1
            else:
                list_of_key = list(stack_top.keys())
                list_of_value = list(stack_top.values())
                for i in range(len(list_of_value)):
                    if list_of_value[i] == 1:
                        mid_dict[list_of_key[i]] = list_of_value[i]

                for k in range(int(len(mid_dict) / 2)):
                    the_one_key_value = mid_dict.popitem()
                    the_one_key = the_one_key_value[0]
                    the_one_order = int(the_one_key.split('_')[1])

                    the_second_key_value = mid_dict.popitem()
                    the_second_key = the_second_key_value[0]
                    the_second_order = int(the_second_key.split('_')[1])
                    matrix_d[the_one_order - 1][the_second_order - 1] += 1
                    matrix_d[the_second_order - 1][the_one_order - 1] += 1

            # 更新邻接矩阵输入你的序列(空格作为分割)
            # count = 0
            while len(stack) != 0:
                # count += 1
                stack_next = stack.pop()
                list_of_next_key = list(stack_next.keys())
                list_of_top_key = list(stack_top.keys())

                for key in list_of_next_key:
                    if key not in list_of_top_key:
                        top_key_not_innext = key

                top_not_innext_order = int(top_key_not_innext.split('_')[1])
                for key in list_of_top_key:
                    if stack_next[key] == stack_top[key] + 1:
                        key_order = int(key.split('_')[1])
                        matrix_d[key_order - 1][top_not_innext_order - 1] += 1
                        matrix_d[top_not_innext_order - 1][key_order - 1] += 1

                # print("第{}次".format(count))
                # print(matrix_d)
                stack_top = stack_next
        else:
            # 输入的序列全部为0
            pass

    return matrix_d,support_flag


def generate_graph():
    Support_Flag = True
    input_str = input_entry.get()
    num = input_str.split()

    num.sort(reverse=True)
    print("正序后: ",num)

    #将输入转化为np数组
    d = np.array(num)
    n = len(d)

    #生成一个nxn的邻接矩阵，用来存放结果
    matrix_d = np.zeros((n,n))


    # 将输入序列变为字典
    d_dict = {}
    for i in range(len(d)):
        key_str = 'v_{}'.format(i+1)
        d_dict[key_str] = int(d[i])

    print(d_dict)




    G = nx.Graph()
    Matrix,Support_Flag =Get_Matrix(d_dict,matrix_d)

    if Support_Flag == True:
        for i in range(len(Matrix)):
            row_sum = 0
            for j in range(len(Matrix)):
                row_sum += Matrix[i,j]
                if Matrix[i, j] != 0:
                    G.add_edge(i+1,j+1)
            if row_sum == 0:
                # 第 i+1 个节点为孤立点
                G.add_node(i+1)

        var.set('可图序列')
        nx.draw_networkx(G,with_labels=True,font_weight='bold')
        plt.show()

    else:
        var.set('否')


generate_button = tk.Button(root, text="生成图形", command=generate_graph)
generate_button.pack()


# 运行主循环
root.mainloop()





















