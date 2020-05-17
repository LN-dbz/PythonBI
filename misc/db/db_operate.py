from flask import Blueprint, request, abort, jsonify
from misc.db.database import db_session

from jinja2 import TemplateNotFound
from datetime import datetime
from misc.score import sort_out_excel, score_analysis
from misc.db.models import User, ExamScore, Exam


# 上传文件
def upload_score_db(parm_dict, file):
    # 是否新建数据
    if parm_dict.get('new_exam', True) and db_session.query(Exam).filter(Exam.name == parm_dict['examName']).count() > 0:
        return {'code': -1, 'message': '考试名称重复！'}

        # 考试信息
    if parm_dict.get('new_exam', True):
        exam = Exam(name=parm_dict['examName'],
                    add_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    start_date=parm_dict['start_end'][0:parm_dict['start_end'].index(' - ')].strip(),
                    end_date=parm_dict['start_end'][parm_dict['start_end'].index(' - ')+3:-1].strip()
                    )
        db_session.add(exam)
        db_session.commit()

    score_list, primary_id_error = sort_out_excel(file, exam_name=parm_dict['examName'])
    for v in score_list:
        if v['primary_id'] not in primary_id_error:
            try:
                db_session.add(ExamScore(**v))
                db_session.commit()
            except:
                primary_id_error.append(v['primary_id'])
    if not primary_id_error:
        return {'code': 0, 'message': f'共{len(score_list)}条数据'}
    else:
        return {'code': 0, 'message': f'共{len(score_list)}条数据提交成功，{len(primary_id_error)}条数据存在重复',
                'data': primary_id_error}


# 主页面显示
def exam_score_analysis_db(exam_name):
    score_list = [v.to_json() for v in ExamScore.query.filter(ExamScore.examName == exam_name).all()]
    result_list = score_analysis(score_list)
    return result_list


# 考试信息
def exam_infer_db(otype='list'):
    if otype == 'list':
        return [v.to_json() for v in Exam.query.order_by(Exam.id.desc()).all()]

# 考试信息
def examscore_infer_db(otype='list',exam=''):
    if otype == 'list':
        return [v.to_json() for v in ExamScore.query.filter(ExamScore.examName == exam).order_by(ExamScore.rank.asc()).all()]


if __name__ == '__main__':
    print(exam_score_analysis_db('驱蚊器委屈q1we34w'))