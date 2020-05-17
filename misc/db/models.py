from sqlalchemy import Column, Integer, String, Float
from misc.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Float, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User name>'


# 考试
class Exam(Base):
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    add_date = Column(String(50))
    start_date = Column(String(50))
    end_date = Column(String(50))

    def __init__(self, name=None, add_date=None, start_date=None, end_date=None):
        self.name = name
        self.add_date = add_date
        self.start_date = start_date
        self.end_date = end_date

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


# 分数
class ExamScore(Base):
    __tablename__ = 'exam_score'
    id = Column(Integer, primary_key=True)
    primary_id = Column(String(250), unique=True)
    name = Column(String(50))
    studentID = Column(String(50))
    className = Column(String(50))
    examID = Column(String(50))
    examName = Column(String(120))

    rank = Column(Integer)
    len = Column(Integer)
    sum = Column(Float)
    svg = Column(Float)

    language = Column(Float)
    math = Column(Float)
    english = Column(Float)
    history = Column(Float)
    biological = Column(Float)
    geography = Column(Float)
    political = Column(Float)

    def __init__(self, studentID=None, className=None, examID=None, examName=None, rank=None, svg=None, name=None,
                 sum=None, language=None, math=None, english=None, history=None, biological=None, geography=None,
                 len=None, political=None, primary_id=None):
        self.len = len
        self.primary_id = primary_id
        self.political = political
        self.studentID = studentID
        self.className = className
        self.examID = examID
        self.examName = examName
        self.rank = rank
        self.svg = svg
        self.name = name
        self.sum = sum
        self.language = language
        self.math = math
        self.english = english
        self.history = history
        self.biological = biological
        self.geography = geography

    def __repr__(self):
        return f'<ExamScore examName>'

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict