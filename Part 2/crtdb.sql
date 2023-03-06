CREATE TABLE Video (
    videoCode   INTEGER PRIMARY KEY,
    videoLength INTEGER
);

CREATE TABLE Model (
    modelNo    CHAR (10)      PRIMARY KEY,
    width      NUMERIC (6, 2),
    height     NUMERIC (6, 2),
    weight     NUMERIC (6, 2),
    depth      NUMERIC (6, 2),
    screenSize NUMERIC (6, 2) 
);

CREATE TABLE Site (
    siteCode INTEGER       PRIMARY KEY,
    type     VARCHAR (16),
    address  VARCHAR (100),
    phone    VARCHAR (16) 
);

CREATE TABLE DigitalDisplay (
    serialNo        CHAR (10) PRIMARY KEY,
    schedulerSystem CHAR (10),
    modelNo         CHAR (10) REFERENCES Model (modelNo) 
);

CREATE TABLE Client (
    clientId INTEGER       PRIMARY KEY,
    name     VARCHAR (40),
    phone    VARCHAR (40),
    address  VARCHAR (100) 
);

CREATE TABLE TechnicalSupport (
    empID  INTEGER      PRIMARY KEY,
    name   VARCHAR (40),
    gender CHAR (1) 
);

CREATE TABLE Administrator (
    empID  INTEGER      PRIMARY KEY,
    name   VARCHAR (40),
    gender CHAR (1) 
);

CREATE TABLE Salesman (
    empID  INTEGER      PRIMARY KEY,
    name   VARCHAR (40),
    gender CHAR (1) 
);

CREATE TABLE AirtimePackage (
    packageID INTEGER      PRIMARY KEY,
    class     VARCHAR (16),
    startDate DATE,
    lastDate  DATE,
    frequency INTEGER,
    videoCode INTEGER
);

CREATE TABLE AdmWorkHours (
    empID INTEGER REFERENCES Administrator (empID),
    day   DATE,
    hours NUMERIC (4, 2),
    PRIMARY KEY (empID, day)
);

CREATE TABLE Broadcasts (
    videoCode INTEGER REFERENCES Video (videoCode),
    siteCode  INTEGER REFERENCES Site (siteCode),
    PRIMARY KEY (videoCode, siteCode)
);

CREATE TABLE Administers (
    empId    INTEGER REFERENCES Administrator (empId),
    siteCode INTEGER REFERENCES Site (siteCode),
    PRIMARY KEY (empId, siteCode)
);

CREATE TABLE Specializes (
    empId   INTEGER   REFERENCES TechnicalSupport (empId),
    modelNo CHAR (10) REFERENCES Model (modelNo),
    PRIMARY KEY (empId, modelNo)
);

CREATE TABLE Purchases (
    clientId       INTEGER REFERENCES Client (clientId),
    empId          INTEGER REFERENCES Salesman (empId),
    packageId      INTEGER REFERENCES AirtimePackage (packageId),
    commissionRate NUMERIC (4, 2), 
    PRIMARY KEY (clientId, empId, packageId)
);

CREATE TABLE Locates (
    serialNo CHAR (10) REFERENCES DigitalDisplay (serialNo),
    siteCode INTEGER   REFERENCES Site (siteCode),
    PRIMARY KEY (serialNo, siteCode)
);

