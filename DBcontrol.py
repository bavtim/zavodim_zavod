
from DBdriver import engine, UsersData, Session


def add_user_info(user_id,pSQL_dbname,pSQL_dbuser,pSQL_dbpassword,pSQL_dbhost):
    with Session(bind=engine) as session:
        UserEpta = UsersData(
            user_id=user_id,
            pSQL_dbname=pSQL_dbname,
            pSQL_dbuser=pSQL_dbuser,
            pSQL_dbpassword=pSQL_dbpassword,
            pSQL_dbhost=pSQL_dbhost,
        )
        session.add_all([UserEpta])
        session.commit()

def getDBdataUsers(user_id):
    temp = []
    with Session(bind=engine) as session:
        db = session.query(UsersData).filter_by(user_id=user_id).all()
        for p in db:
            temp.append(p.as_dict())
    return temp

# def test_init():
#     add_user_info(1,"1","1","1","1")
#     add_user_info(1, "1", "1", "1", "1")
#     add_user_info(2, "1", "1", "1", "1")
#     print(getDBdataUsers(1))

# test_init()