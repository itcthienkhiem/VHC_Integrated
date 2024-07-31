import psycopg2
import order_model
from fastapi import HTTPException
from collections import namedtuple

from typing import List

def connect_to_db():
  """Kết nối đến cơ sở dữ liệu SQLite3.

  Args:
    db_file: Đường dẫn đến tệp cơ sở dữ liệu.

  Returns:
    Kết nối đến cơ sở dữ liệu.
  """

  try:
      conn = psycopg2.connect(
          database="IntegratedDB",
          user="postgres",
          password="123456",
          host="localhost",
          port="5432")
      return conn
  except psycopg2.Error as e:
      print(f"Lỗi khi kết nối đến cơ sở dữ liệu: {e}")
      return None


def get_order(query):
    conn = connect_to_db()
    data = conn.execute(query).fetchall()
    conn.close()
    return data

def get_order_by_id(order_id):
    conn = connect_to_db()
    sql= '''SELECT * FROM Orders WHERE Orders.OrderID=?'''
    data = conn.execute(sql,(order_id,)).fetchone()
    conn.close()
    return data

def get_order_by_accessionNumber(accessionNumber):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        print ('exce get_order_by_accessionNumber')
        sql= '''SELECT * FROM Orders WHERE accessionNumber=%s'''
        cursor.execute(sql,(accessionNumber,))
        data  = cursor.fetchone()
        if data is None:
            return None
        order = order_model.Orders
        order.id = data[0]
        order.accessionNumber = data[1]
        order.requestedDepartmentCode = data[2]
        order.requestedDepartmentName = data[3]
        order.referringPhysicianCode = data[4]
        order.referringPhysicianName = data[5]
        order.clinicalDiagnosis = data[6]
        order.inpatient = data[7]
        order.urgent = data[8]
        order.orderDatetime = data[9]
        order.modalityType = data[10]
        order.insuranceApplied = data[11]
        order.insuranceNumber = data[12]
        order.orderNumber = data[13]
        order_model.Orders = order
        #print(row)
        sql= '''SELECT * FROM patient WHERE IdOrder=%s'''

        cursor.execute(sql,(order.id,))
        patient =cursor.fetchone()
        if patient is None:
            return None
        pt = order_model.Patient
        pt.id = patient[0]
        pt.pid = patient[1]
        pt.fullname= patient[2]
        pt.gender = patient[3]
        pt.birthDate= patient[4]
        pt.address= patient[5]
        pt.idOrder= patient[6]
        order.patient   = pt

        #order_model.Orders=namedtuple('order_model.Orders', 'id orderNumber accessionNumber requestedDepartmentCode requestedDepartmentName referringPhysicianCode referringPhysicianName clinicalDiagnosis inpatient urgent orderDatetime modalityType insuranceApplied insuranceNumber')
        #row = cursor.fetchone()
        sql = '''SELECT * FROM Services WHERE IdOrder=%s'''
        cursor.execute(sql, (order.id,))
        svs = cursor.fetchall()
        if svs is None:
            return None
       # sv_list = order_model.Service(order.service=[])
        order.service= []
        for id,requestedProcedureCode, requestedProcedureName, idOrder in svs:
            msv = order_model.Service
            msv.id = id
            msv.requestedProcedureCode = requestedProcedureCode
            msv.requestedProcedureName = requestedProcedureName
            msv.idOrder = idOrder

            order.service.append(msv)

        print('exce get all get_order_by_accessionNumber complete')

    #orders = [order_model.Orders(*row) for row in cursor.fetchall()]
    #for ord in orders:
    #    print(ord.id, ord.orderNumber, ord.accessionNumber)

    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        raise e
    finally:
        cursor.close()
        conn.close()

    return order

def insert_result(result: order_model.Result):

    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        print('start insert result')
        #Tim trong table Orders xem co ton tai chi dinh nao khong, neu co thi lay order_id ra va insert vao db
        sql = '''SELECT id FROM Orders WHERE AccessionNumber=%s'''
        cursor.execute(sql, (result.accessionNumber,))
        svs = cursor.fetchone()
        # sv_list = order_model.Service(order.service=[])
        order_id = svs[0]
        if svs is None:
            return None
        sql_order = '''INSERT INTO Result (Descript, Conclude, IdOrder,AccessionNumber, study) VALUES (%s, %s, %s,%s,%s)'''
        cursor.execute(sql_order, (result.descript,result.conclude, order_id,result.accessionNumber,result.study))
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        raise e
    finally:
        cursor.close()
        conn.close()

def get_result(accessionNumber:str):
    result = order_model.Result
    conn = connect_to_db()
    cursor = conn.cursor()
    try:

        print('start get_result')
        #Tim trong table Orders xem co ton tai chi dinh nao khong, neu co thi lay order_id ra va insert vao db
        sql = '''SELECT * FROM Result WHERE AccessionNumber=%s'''

        cursor.execute(sql, (accessionNumber,))
        data = cursor.fetchone()
        # sv_list = order_model.Service(order.service=[])
        if data is None:
            return None
        return data

    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        raise e
    finally:
        cursor.close()
        conn.close()

    return result

def insert_order(order:order_model.Orders):
    print("start insert db")

    conn = connect_to_db()
    cursor = conn.cursor()

    try:


        print('start insert orders')
        cursor.execute("INSERT INTO orders (orderNumber,accessionNumber, requestedDepartmentCode,requestedDepartmentName,referringPhysicianCode,referringPhysicianName,clinicalDiagnosis,inpatient,urgent,orderDatetime,modalityType,insuranceApplied,insuranceNumber) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)  RETURNING id",
                       (order.orderNumber,order.accessionNumber,
                        order.requestedDepartmentCode,order.requestedDepartmentName,
                        order.referringPhysicianCode,order.referringPhysicianName,
                        order.clinicalDiagnosis, order.inpatient, order.urgent,order. orderDatetime, order.modalityType,order. insuranceApplied,
                        order.insuranceNumber
                        ))
        order_id = cursor.fetchone()[0]

        print('start insert patient')
        sql_order = '''INSERT INTO patient (pid, fullname, gender,birthDate,address,IdOrder) VALUES (%s, %s, %s,%s,%s,%s)'''
        cursor.execute(sql_order, (order.patient.pid, order.patient.fullname,order.patient. gender,order.patient.birthDate,order.patient.address,order_id))
        print('start insert services')


        for serv in order.services:
            sql_services = '''INSERT INTO services (RequestedProcedureCode,RequestedProcedureName,IdOrder) VALUES (%s, %s, %s)'''
            cursor.execute(sql_services, (serv.requestedProcedureCode, serv.requestedProcedureName,order_id))


        conn.commit()

    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        raise e
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
  print(get_order("select * from orders"))
