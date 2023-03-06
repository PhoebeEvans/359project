PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Video
INSERT INTO Video (videoCode, videoLength) VALUES (1001, 5);
INSERT INTO Video (videoCode, videoLength) VALUES (1002, 2);
INSERT INTO Video (videoCode, videoLength) VALUES (1003, 7);
INSERT INTO Video (videoCode, videoLength) VALUES (1004, 1);
INSERT INTO Video (videoCode, videoLength) VALUES (1005, 3);

-- Table: Model
INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES ('1234AB', 4, 6, 3, 2, 5);
INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES ('10246PNV', 4, 4, 4, 4, 4);
INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES ('14443MTE', 4, 4, 4, 3, 6);
INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES ('1138EM', 6, 4, 2, 2, 5);
INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES ('1487WOR', 3, 5, 2, 4, 3);

-- Table: Site
INSERT INTO Site (siteCode, type, address, phone) VALUES (1001, 'Restaurant', '3450 Aviation Ave, Anchorage, AK 99502', '907-249-4444');
INSERT INTO Site (siteCode, type, address, phone) VALUES (1002, 'Restaurant', '247 Otto Lake Rd., Healy, AK 99743', '907-683-4653');
INSERT INTO Site (siteCode, type, address, phone) VALUES (1003, 'Restaurant', '810 Front St., Leadville, CO 80461', '719-486-0749');
INSERT INTO Site (siteCode, type, address, phone) VALUES (1004, 'Restaurant', '2846 CO-300, Leadville, CO 80461', '719-486-0189');
INSERT INTO Site (siteCode, type, address, phone) VALUES (1005, 'Restaurant', '1747 Jarrettsville Rd, Jarrettsville, MD 21084', '410-692-5100');

-- Table: DigitalDisplay
INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES ('1001', 'Original', '1234AB');
INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES ('1455', 'Rose', '1487WOR');
INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES ('141312M', 'Rocky', '14443MTE');
INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES ('1860A26', 'Gold', '10246PNV');
INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES ('1066EM', 'Marshal', '1138EM');

-- Table: Client
INSERT INTO Client (clientId, name, phone, address) VALUES (101, 'Calista Langley', '719-486-1229', '510 Harrision Ave., Leadville, CO 80461');
INSERT INTO Client (clientId, name, phone, address) VALUES (102, 'Theoderic Garrison', '508-693-0455', '636 Old Country Rd., West Tisbury, MA 02575');
INSERT INTO Client (clientId, name, phone, address) VALUES (103, 'Amelia de Clare', '44-24-7688-7688', 'Much Hadham, England, SG10 6AA United Kingdom');
INSERT INTO Client (clientId, name, phone, address) VALUES (104, 'Lillian Stuart', '719-486-0749', '2425 Co Rd. 5, Fairplay CO 80440');
INSERT INTO Client (clientId, name, phone, address) VALUES (105, 'John Hamilton', '410-969-5567', '2999 Ayres Chapel Rd., White Hall, MD 21161');

-- Table: TechnicalSupport
INSERT INTO TechnicalSupport (empID, name, gender) VALUES (301, 'Nikola Jokic', 'm');
INSERT INTO TechnicalSupport (empID, name, gender) VALUES (302, 'Aaron Gordon', 'm');
INSERT INTO TechnicalSupport (empID, name, gender) VALUES (303, 'Jamaal Murray', 'm');
INSERT INTO TechnicalSupport (empID, name, gender) VALUES (304, 'Michael Porter Jr.', 'm');
INSERT INTO TechnicalSupport (empID, name, gender) VALUES (305, 'Kentavious Caldwell-Pope', 'm');

-- Table: Administrator
INSERT INTO Administrator (empID, name, gender) VALUES (401, 'Phoebe Evans', 'f');
INSERT INTO Administrator (empID, name, gender) VALUES (402, 'Lauren Glaser', 'f');
INSERT INTO Administrator (empID, name, gender) VALUES (403, 'Ty Bergman', 'm');
INSERT INTO Administrator (empID, name, gender) VALUES (404, 'Florence Nightingale', 'f');
INSERT INTO Administrator (empID, name, gender) VALUES (405, 'Marcus Aurelius', 'm');

-- Table: Salesman
INSERT INTO Salesman (empID, name, gender) VALUES (201, 'Bilbo Baggins', 'm');
INSERT INTO Salesman (empID, name, gender) VALUES (202, 'Arwen Evenstar', 'f');
INSERT INTO Salesman (empID, name, gender) VALUES (203, 'Legolas Greenleaf', 'm');
INSERT INTO Salesman (empID, name, gender) VALUES (204, 'Eowyn Rohir', 'f');
INSERT INTO Salesman (empID, name, gender) VALUES (205, 'Tom Bombadil', 'm');

-- Table: AirtimePackage
INSERT INTO AirtimePackage (packageID, class, startDate, lastDate, frequency, videoCode) VALUES (90100, 'First', '2023-03-01', '2023-03-02', 3, 5);
INSERT INTO AirtimePackage (packageID, class, startDate, lastDate, frequency, videoCode) VALUES (90101, 'First', '2023-02-28', '2023-03-02', 1, 1);
INSERT INTO AirtimePackage (packageID, class, startDate, lastDate, frequency, videoCode) VALUES (90102, 'First', '2023-02-24', '2023-02-28', 2, 3);
INSERT INTO AirtimePackage (packageID, class, startDate, lastDate, frequency, videoCode) VALUES (90103, 'Second', '2023-03-01', '2023-03-02', 2, 6);
INSERT INTO AirtimePackage (packageID, class, startDate, lastDate, frequency, videoCode) VALUES (90104, 'First', '2023-02-27', '2023-03-01', 1, 1);

-- Table: AdmWorkHours
INSERT INTO AdmWorkHours (empID, day, hours) VALUES (401, '2023-03-01', 8);
INSERT INTO AdmWorkHours (empID, day, hours) VALUES (402, '2023-03-01', 8);
INSERT INTO AdmWorkHours (empID, day, hours) VALUES (403, '2023-03-01', 8);
INSERT INTO AdmWorkHours (empID, day, hours) VALUES (404, '2023-03-01', 10);
INSERT INTO AdmWorkHours (empID, day, hours) VALUES (405, '2023-03-01', 10);

-- Table: Broadcasts
INSERT INTO Broadcasts (videoCode, siteCode) VALUES (1001, 1001);
INSERT INTO Broadcasts (videoCode, siteCode) VALUES (1001, 1004);
INSERT INTO Broadcasts (videoCode, siteCode) VALUES (1003, 1002);
INSERT INTO Broadcasts (videoCode, siteCode) VALUES (1005, 1005);
INSERT INTO Broadcasts (videoCode, siteCode) VALUES (1002, 1003);

-- Table: Administers
INSERT INTO Administers (empId, siteCode) VALUES (401, 1001);
INSERT INTO Administers (empId, siteCode) VALUES (402, 1002);
INSERT INTO Administers (empId, siteCode) VALUES (403, 1004);
INSERT INTO Administers (empId, siteCode) VALUES (403, 1003);
INSERT INTO Administers (empId, siteCode) VALUES (405, 1005);

-- Table: Specializes
INSERT INTO Specializes (empId, modelNo) VALUES (301, '14443MTE');
INSERT INTO Specializes (empId, modelNo) VALUES (302, '14443MTE');
INSERT INTO Specializes (empId, modelNo) VALUES (303, '10246PNV');
INSERT INTO Specializes (empId, modelNo) VALUES (304, '1138EM');
INSERT INTO Specializes (empId, modelNo) VALUES (305, '1487WOR');

-- Table: Purchases
INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES (101, 201, 90100, 3);
INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES (103, 202, 90101, 2);
INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES (104, 204, 90102, 4);
INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES (105, 203, 90104, 2);
INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES (102, 205, 90102, 3);

-- Table: Locates
INSERT INTO Locates (serialNo, siteCode) VALUES ('1455', 1003);
INSERT INTO Locates (serialNo, siteCode) VALUES ('141312M', 1004);
INSERT INTO Locates (serialNo, siteCode) VALUES ('1860A26', 1005);
INSERT INTO Locates (serialNo, siteCode) VALUES ('1066EM', 1001);
INSERT INTO Locates (serialNo, siteCode) VALUES ('1455', 1002);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
