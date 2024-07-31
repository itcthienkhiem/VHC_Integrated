from pydantic import BaseModel
from typing import List
class Service(BaseModel):
    id: int| None = None
    requestedProcedureCode: str| None = None
    requestedProcedureName: str| None = None
    idOrder: int| None = None

class Patient(BaseModel):
    pid: str| None = None
    fullname: str| None = None
    gender: str| None = None
    birthDate: str| None = None
    address: str| None = None
    idOrder :int| None = None
class Orders(BaseModel):
    id: int| None = None
    orderNumber: str| None = None
    accessionNumber: str| None = None
    requestedDepartmentCode: str| None = None
    requestedDepartmentName: str| None = None
    referringPhysicianCode: str| None = None
    referringPhysicianName: str| None = None
    clinicalDiagnosis: str| None = None
    inpatient: int| None = None
    urgent: int| None = None
    orderDatetime: str| None = None
    modalityType: str| None = None
    patient: Patient| None = None
    services: List[Service]| None = None
    insuranceApplied: int| None = None
    insuranceNumber: str| None = None

class Result(BaseModel):
    id: int| None = None
    descript: str| None = None
    conclude: str| None = None
    idOrder: int| None = None
    accessionNumber: str| None = None
    study: str| None = None

def get_result_XML(r:Result):
    if r is None :
        return []
    path = 'https://cdha.viethealthcareclinic.com/viewer?StudyInstanceUIDs='
    return {
        "accessionNumber": r[4],
        "descript": r[1],
        "conclude": r[2],
        "url": path+ r[5]
    }

def get_order_XML(o: Orders):
    if o is None :
        return None
    xml_sv =[]
    svs = o.service;
    i = 0
    while i < len(svs):
        dt = {
            "id": svs[i].id,
            "requestedProcedureCode": svs[i].requestedProcedureCode,
            "requestedProcedureName": svs[i].requestedProcedureName,
            "idOrder": svs[i].idOrder,

        }
        xml_sv.append(dt)
        i = i + 1





    return {
	"orderNumber": o.orderNumber,
	"accessionNumber": o.accessionNumber,
	"requestedDepartmentCode": o.requestedDepartmentCode,
	"requestedDepartmentName": o.requestedDepartmentName,
	"referringPhysicianCode": o.referringPhysicianCode,
	"referringPhysicianName": o.referringPhysicianName,
	"clinicalDiagnosis": o.clinicalDiagnosis,
	"inpatient": o.inpatient,
	"urgent": o.urgent,
	"orderDatetime": o.orderDatetime,
	"modalityType": o.modalityType,
	"patient": {
    	"pid": o.patient.pid,
    	"fullname": o.patient.fullname,
    	"gender": o.patient.gender,
    	"birthDate": o.patient.birthDate,
    	"address": o.patient.address,
	},
	"services": xml_sv,
	"insuranceApplied": o.insuranceApplied,
	"insuranceNumber": o.insuranceNumber,
}


