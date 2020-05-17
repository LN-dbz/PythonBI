from collections import defaultdict
from flask import Blueprint, request, send_from_directory, jsonify
from misc.db.db_operate import upload_score_db, exam_score_analysis_db, exam_infer_db, examscore_infer_db

subject_map = {'language': '语文', 'math': '数学', 'english': '英语', 'political': '政治', 'history': '历史', 'biological': '生物',
               'geography': '地理'}
subject_list_zh = ['语文', '数学', '英语', '政治', '历史', '生物', '地理']

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api/down/<exam_name>', methods=['GET'])
def down_score_excel(exam_name):
    print(exam_name)
    return send_from_directory('data_folder/',exam_name,as_attachment=True)

@api.route('/api/upload', methods=['POST'])
def upload_score():
    """
    成绩文件上传，导入数据库
    :return:
    """
    if request.files['file'].filename[request.files['file'].filename.index('.') + 1:-1] not in ['xls', 'xlsx']:
        return jsonify({'code': -1, 'message': '文件格式错误！'})
    parm_dict = request.form
    return jsonify(upload_score_db(parm_dict, request.files['file']))


@api.route('/api/exam_score_analysis', methods=['get'])
def exam_score_analysis():
    exam_name = request.values.get('exam_name')
    result_list = exam_score_analysis_db(exam_name)
    subject_svg_d = {'subject': [], '平均分': [], '最低分': [], '最高分': []}
    for k, v in result_list['subject_svg_d'].items():
        subject_svg_d['subject'].append(subject_map[k])
        subject_svg_d['平均分'].append(v['svg'])
        subject_svg_d['最低分'].append(v['min'])
        subject_svg_d['最高分'].append(v['max'])
    result_list['subject_svg_d'] = subject_svg_d
    subject_difficulty = {'subject': [], 'svg': [], 'diff': [], 'pass': []}
    for k, v in result_list['subject_difficulty'].items():
        subject_difficulty['subject'].append(subject_map[k])
        subject_difficulty['svg'].append(v['svg'])
        subject_difficulty['diff'].append(v['diff'])
        subject_difficulty['pass'].append(v['pass'])
    subject_distributed = {'subject': subject_list_zh,
                           'distributed': ['00-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80',
                                           '80-90', '90-100', '100-110', '110-120'],
                           'distributed_list': []}
    distributed_list = defaultdict(lambda: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for k, v in result_list['subject_distributed'].items():
        for __k, __v in v.items():
            distributed_list[k][subject_distributed['distributed'].index(__k)] = __v
    for k, v in distributed_list.items():
        subject_distributed['distributed_list'].append({
            'name': subject_map[k],
            'type': 'line',
            'areaStyle': {},
            'data': v
        })
    result_list['subject_distributed'] = subject_distributed
    result_list['subject_difficulty'] = subject_difficulty

    subject_pph = {'subject': subject_list_zh, 'low': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   'pass': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'high': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    for k, v in result_list['subject_pph'].items():
        subject_pph['low'][subject_list_zh.index(subject_map[k])] = v['low']
        subject_pph['pass'][subject_list_zh.index(subject_map[k])] = v['pass']
        subject_pph['high'][subject_list_zh.index(subject_map[k])] = v['high']
    result_list['subject_pph'] = subject_pph
    result_list['score_font_20'] = {'score': [], 'name': []}
    for v_index, v in enumerate(examscore_infer_db(otype='list', exam=exam_name)):
        if v_index >= 20:
            break
        result_list['score_font_20']['score'].append(v['sum'])
        result_list['score_font_20']['name'].append(v['name'])

    result_list['score_font_20']['score'] =result_list['score_font_20']['score'][::-1]
    result_list['score_font_20']['name'] = result_list['score_font_20']['name'][::-1]
    return jsonify(result_list)


@api.route('/api/exam_list', methods=['get'])
def exam_list():
    return jsonify({'code': 0, 'data': exam_infer_db(otype='list')})
