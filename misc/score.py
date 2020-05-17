import pandas as pd
from pathlib import Path
from collections import defaultdict

# 主要信息 columns
must_columns = ['学号', '班级', '考号', '姓名', '考试名称', '排名', '姓名']
# 科目map
subject_map = {'语文': 'language', '数学': 'math', '英语': 'english', '政治': 'political', '历史': 'history',
               '生物': 'biological', '地理': 'geography'}
# 科目分数分级
subject_score = {'language': {'full': 120, 'pass': 80, 'high': 100}, 'math': {'full': 120, 'pass': 80, 'high': 100},
                 'english': {'full': 120, 'pass': 80, 'high': 100}, 'political': {'full': 120, 'pass': 80, 'high': 100},
                 'history': {'full': 120, 'pass': 80, 'high': 100},
                 'biological': {'full': 120, 'pass': 80, 'high': 100},
                 'geography': {'full': 120, 'pass': 80, 'high': 100}}

subject_list = ['language', 'math', 'english', 'political', 'history', 'biological', 'geography']
# 主要信息map
index_map = {'学号': 'studentID', '班级': 'className', '考号': 'examID', '姓名': 'name', '排名': 'rank', '考试名称': 'examName'}


# 整理excel
def sort_out_excel(f_path, exam_name=None):
    """
    :param f_path: 文件路径
    :param exam_name: 考试名称
    :return: 处理后的数据 dict_list
    """
    # 不存在文件直接跳过
    if isinstance(f_path, str) and not Path(f_path).is_file:
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
    primary_id_list = []
    primary_id_error = []
    for row_index, row in enumerate(pf.values):
        # 将数据补 0
        rows = [v if isinstance(v, str) or isinstance(v, float) or isinstance(v, int) else 0 for v in list(row)]
        # 主要信息
        main_infer = {v: rows[k] for k, v in index_map_sorted.items()}
        main_infer['primary_id'] = f"{main_infer['studentID']}_{main_infer['examName']}"
        if main_infer['primary_id'] in primary_id_list:
            primary_id_error.append(main_infer['primary_id'])
        else:
            primary_id_list.append(main_infer['primary_id'])
        # 科目信息
        subject_infer = {v: rows[k] for k, v in index_subject_sorted.items()}
        # 计算本次信息的数据
        eval_infer = {'sum': 0, 'svg': 0, 'len': 0}
        for v in subject_infer.values():
            eval_infer['sum'] += v
            eval_infer['len'] += 1
        eval_infer['svg'] = str(eval_infer['sum'] / eval_infer['len'])
        if '.' in eval_infer['svg'] and len(eval_infer['svg']) - eval_infer['svg'].index('.') > 2:
            eval_infer['svg'] = eval_infer['svg'][0:2 + eval_infer['svg'].index('.')]
        eval_infer['svg'] = float(eval_infer['svg'])
        eval_infer.update(main_infer)
        eval_infer.update(subject_infer)
        result_list.append(eval_infer)
    pf.to_excel(f'data_folder/{exam_name}.xlsx')
    return result_list, primary_id_error


def two_value(value):
    value = str(value)
    if '.' in value and len(value) - value.index('.') > 2:
        value = value[0:2 + value.index('.')]
    return float(value)


# 成绩分析
def score_analysis(score_list):
    # 成绩分布
    subject_sum = defaultdict(int)
    # 成绩分布情况 https://echarts.apache.org/examples/zh/editor.html?c=area-stack
    subject_distributed = defaultdict(lambda: defaultdict(int))
    # 成绩集合
    subject_score_list = defaultdict(list)
    # 高分率、及格率、低分率
    subject_pph = defaultdict(lambda: {'high': 0, 'pass': 0, 'low': 0})
    # 总分list
    total_eval = {'sum_svg': 0, 'sum_list': []}
    person_num = len(score_list)
    for score_obj in score_list:

        for subject_name in subject_list:
            subject_sum[subject_name] += score_obj[subject_name]
            subject_distributed[subject_name][score_grade(score_obj[subject_name])] += 1
            subject_score_list[subject_name].append(score_obj[subject_name])
            # 高分率
            subject_pph[subject_name][score_ppl(subject_name, score_obj[subject_name])] += 1
        # 总分
        total_eval['sum_svg'] += score_obj['sum']
        total_eval['sum_list'].append(score_obj['sum'])

    # 每一科的平均值
    subject_svg = {v: two_value(subject_sum[v] / person_num) for v in subject_sum}
    # 每一科的平局分最低分最高分
    subject_svg_d = {v: {'svg': subject_svg[v], 'max': two_value(max(subject_score_list[v])),
                         'min': two_value(min(subject_score_list[v]))}for v in subject_score_list}
    # 总平局分
    total_eval['sum_svg'] = total_eval['sum_svg'] / len(score_list)
    # 难度系数 及格率 平均分数
    subject_difficulty = {k: {'diff': two_value(1-v/subject_score[k]['full']), 'svg': v,
                              'pass': two_value((subject_pph[k]['pass'] + subject_pph[k]['high'])/person_num)}
                          for k, v in subject_svg.items()}
    result_dict = {
        # 总平局分
        'sum_svg': two_value(total_eval['sum_svg']),
        # 每一科的平均值
        'subject_svg': subject_svg,
        # 每一科的难度系数
        'subject_difficulty': subject_difficulty,
        # 每一科的平局分最高分最低分
        'subject_svg_d': subject_svg_d,
        # 高分率、及格率、低分率
        'subject_pph': subject_pph,
        # 成绩分布
        'subject_distributed': subject_distributed
    }
    return result_dict


# 分数等级分级
def score_grade(value):
    value = float(value)
    return f'{int(value // 10)}0-{int(value // 10 + 1)}0'


# 计算高分率，及格率， 低分率
def score_ppl(name, value):
    score_obj = subject_score[name]
    if value < score_obj['pass']:
        return 'low'
    elif score_obj['pass'] <= value < score_obj['high']:
        return 'pass'
    else:
        return 'high'


if __name__ == '__main__':
    from datetime import datetime
    now = datetime.now()

    score_list = sort_out_excel('data_folder/score_test.xlsx')
    print(datetime.now()-now)
    s = score_analysis(score_list[0])
    print(datetime.now()-now)
    print(s)