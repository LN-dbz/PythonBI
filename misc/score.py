import pandas as pd
from pathlib import Path

# 主要信息 columns
must_columns = ['学号', '班级', '考号', '姓名', '考试名称']
# 科目map
subject_map = {'语文': 'Language', '数学': 'math', '英语': 'English', '政治': 'political', '历史': 'history',
               '生物': 'biological', '地理': 'Geography'}
# 主要信息map
index_map = {'学号': 'studentID', '班级': 'class', '考号': 'examID', '考试名称': 'examName'}


# 整理excel
def sort_out_excel(f_path, exam_name=None):
    """
    :param f_path: 文件路径
    :param exam_name: 考试名称
    :return: 处理后的数据 dict_list
    """
    # 不存在文件直接跳过
    if not Path(f_path).is_file:
        return {'message': '缺少文件'}
    # 读取文件信息
    pf = pd.read_excel(f_path, dtype={'studentID': str})
    if exam_name:
        pf['考试名称'] = exam_name
    # 验证是否存在必须的列名
    pd_columns = list(pf.columns)
    if [v for v in must_columns if v not in pd_columns]:
        return {'message': '文件格式不正确'}
    # 主要信息index
    index_map_sorted = {pd_columns.index(k): v for k, v in index_map.items()}
    # 科目信息index
    index_subject_sorted = {pd_columns.index(k): v for k, v in subject_map.items()}
    # 转化为dict_list 输出
    result_list = []
    for row in pf.values:
        # 将数据补 0
        rows = [v if isinstance(v, str) or isinstance(v, float) or isinstance(v, int) else 0 for v in list(row)]
        # 主要信息
        main_infer = {v: rows[k] for k, v in index_map_sorted.items()}
        # 科目信息
        subject_infer = {v: rows[k] for k, v in index_subject_sorted.items()}
        # 计算本次信息的数据
        eval_infer = {'sum': 0, 'svg': 0, 'len': 0}
        for v in  subject_infer.values():
            eval_infer['sum'] += v
            eval_infer['len'] += 1
        eval_infer['svg'] = str(eval_infer['sum'] / eval_infer['len'])
        if '.' in eval_infer['svg'] and len(eval_infer['svg']) - eval_infer['svg'].index('.') > 2:
            eval_infer['svg'] = eval_infer['svg'][0:2+eval_infer['svg'].index('.')]
        eval_infer['svg'] = float(eval_infer['svg'])
        eval_infer.update(main_infer)
        eval_infer.update(subject_infer)
        result_list.append(eval_infer)
    return result_list


if __name__ == '__main__':
    print(sort_out_excel('data_folder/score_test.xlsx'))
