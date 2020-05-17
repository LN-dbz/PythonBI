# 初始化
from misc.db.database import Base, engine


def init_db():
    """
    初始化数据文件
    :return:
    """
    from misc.db.models import User
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()