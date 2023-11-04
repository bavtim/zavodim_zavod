
from DBdriver import engine, UsersData, Session

def delete_user_info(id,user_id):
    with Session(bind=engine) as session:
        temp = []
        db = session.query(UsersData).filter_by(id=id).filter_by(user_id=user_id)
        for p in db:
            temp.append(p.as_dict())
        if len(temp)>0:
            db.delete()
            session.commit()
        else:
            raise Exception

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