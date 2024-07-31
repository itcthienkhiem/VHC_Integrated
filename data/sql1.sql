--
-- File generated with SQLiteStudio v3.4.4 on Tue Jul 30 19:52:27 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Orders
DROP TABLE IF EXISTS Orders;

CREATE TABLE IF NOT EXISTS Orders (
    Id                      INTEGER PRIMARY KEY AUTOINCREMENT
                                    NOT NULL,
    AccessionNumber         TEXT,
    RequestedDepartmentCode TEXT,
    RequestedDepartmentName TEXT,
    ReferringPhysicianCode  TEXT,
    ReferringPhysicianName  TEXT,
    ClinicalDiagnosis       TEXT,
    Inpatient               INTEGER,
    Urgent                  INTEGER,
    OrderDatetime           TEXT,
    ModalityType            TEXT,
    InsuranceApplied        INTEGER,
    InsuranceNumber         TEXT,
    OrderNumber             TEXT
);

INSERT INTO Orders (Id, AccessionNumber, RequestedDepartmentCode, RequestedDepartmentName, ReferringPhysicianCode, ReferringPhysicianName, ClinicalDiagnosis, Inpatient, Urgent, OrderDatetime, ModalityType, InsuranceApplied, InsuranceNumber, OrderNumber) VALUES (9, '202312221151912', '240085', 'Khoa khám b?nh da khoa', '1340913', 'Nguy?n Th? Nhu Ng?c', 'I10 - B?nh lý tang huy?t áp; (E90*) R?i lo?n chuy?n hóa và dinh du?ng trong các b?nh dã du?c phân lo?i ? ph?n khác; (I20) Con dau th?t ng?c; (E78) R?i lo?n chuy?n hóa lipoprotein và tình tr?ng tang lipid máu khác; (R10) Ðau b?ng và vùng ch?u; (H81) R?i lo?n ch?c nang ti?n dình; (J20) Viêm ph? qu?n c?p', 0, 0, '20231222082236', 'DX', 1, 'KC2242420481118', '202312221151912');

-- Table: Patient
DROP TABLE IF EXISTS Patient;

CREATE TABLE IF NOT EXISTS Patient (
    Id        INTEGER PRIMARY KEY AUTOINCREMENT
                      NOT NULL,
    Pid       TEXT    NOT NULL,
    Fullname  TEXT    NOT NULL,
    Gender    TEXT,
    BirthDate TEXT,
    Address   TEXT,
    IdOrder   INTEGER REFERENCES Orders (Id) 
);

INSERT INTO Patient (Id, Pid, Fullname, Gender, BirthDate, Address, IdOrder) VALUES (3, '5581807', 'NGÔ QUANG PHÚC', 'M', '19530101', 'Thôn Ngành B?n, Xã Yên M?, Huy?n L?ng Giang, T?nh B?c Giang', 9);

-- Table: Result
DROP TABLE IF EXISTS Result;

CREATE TABLE IF NOT EXISTS Result (
    Id               INTEGER PRIMARY KEY AUTOINCREMENT,
    Descript         TEXT,
    Conclude         TEXT,
    IdOrder          INTEGER REFERENCES Orders (Id),
    AccessionNumber  TEXT,
    StudyInstanceUid TEXT
);

INSERT INTO Result (Id, Descript, Conclude, IdOrder, AccessionNumber, StudyInstanceUid) VALUES (8, 'dây là n?i dung ', 'dây là conclude', 9, '202312221151912', NULL);

-- Table: Services
DROP TABLE IF EXISTS Services;

CREATE TABLE IF NOT EXISTS Services (
    Id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    RequestedProcedureCode TEXT,
    RequestedProcedureName TEXT,
    IdOrder                INTEGER REFERENCES Orders (Id) 
);

INSERT INTO Services (Id, RequestedProcedureCode, RequestedProcedureName, IdOrder) VALUES (3, '37', 'Ch?p Xquang ng?c th?ng', 9);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
