from misc.db.database import db_session
from misc.db.models import User, ExamScore, Exam
from misc.score import sort_out_excel
from misc.init import init_db

init_db()
