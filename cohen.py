# Example usage of Cohen's kappa
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
import pandas as pd

def convert_categories_to_integers(array1, array2):
    # 合并两个数组
    combined_array = pd.Series(array1 + array2)

    # 获取唯一的类别值
    unique_categories = combined_array.dropna().unique()

    # 创建类别到整数的映射
    category_mapping = {category: i+1 for i, category in enumerate(unique_categories)}

    # 将类别转换为整数
    integers1 = [category_mapping.get(category,-1) for category in array1]
    integers2 = [category_mapping.get(category,-1) for category in array2]

    return integers1, integers2

def read_excel_files(file1, file2,ele):
    # 读取Excel文件
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # 获取共有的问题编号id列
    common_ids = list(set(df1['编号']).intersection(df2['编号']))

    # 存储共有问题编号id对应的event类型
    event_types1 = [df1.loc[df1['编号'] == id, ele].values[0] for id in common_ids]
    event_types2 = [df2.loc[df2['编号'] == id, ele].values[0] for id in common_ids]

    return event_types1,event_types2

def read_name(ele):
    # 用法示例，改这里的地址
    file1_path = '/Users/linzheyuan/Desktop/Jira缺陷收集表1.xlsx'
    file2_path = '/Users/linzheyuan/Desktop/Jira缺陷收集表2.xlsx'

    event_types1, event_types2 = read_excel_files(file1_path, file2_path,ele)
    # print(event_types1)
    # print(event_types2)
    integers1, integers2 = convert_categories_to_integers(event_types1, event_types2)
    # print(integers1)
    # print(integers2)
    # Prepare the dataset, suppose you have two datasets in DataFrame format
    raters_1 = pd.DataFrame({'confirm_A': integers1})
    raters_2 = pd.DataFrame({'confirm_B': integers2})

    # Calculate cohen's kappa
    kappa = cohen_kappa_score(raters_1, raters_2)
    print(ele+"kappa = "+str(kappa))

read_name('Event类型')
read_name('Root cause类型')
read_name('Symptom类型')