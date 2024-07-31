--
-- File generated with SQLiteStudio v3.4.4 on Mon Jul 29 15:04:27 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Order
DROP TABLE IF EXISTS [Order];

CREATE TABLE IF NOT EXISTS [Order] (
    Id                      INTEGER PRIMARY KEY AUTOINCREMENT
                                    NOT NULL,
    AccessionNumber         TEXT    NOT NULL,
    RequestedDepartmentCode TEXT,
    RequestedDepartmentName TEXT,
    ReferringPhysicianCode  TEXT,
    ReferringPhysicianName  TEXT,
    ClinicalDiagnosis       TEXT,
    Inpatient               INTEGER,
    Urgent                  INTEGER,
    OrderDatetime           TEXT,
    ModalityType            TEXT,
    PatientId               INTEGER,
    InsuranceApplied        INTEGER,
    InsuranceNumber         TEXT
);


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
    IdOrder   INTEGER REFERENCES [Order] (Id) 
);


-- Table: Services
DROP TABLE IF EXISTS Services;

CREATE TABLE IF NOT EXISTS Services (
    Id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    RequestedProcedureCode TEXT,
    RequestedProcedureName TEXT,
    IdOrder                INTEGER REFERENCES [Order] (Id) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
