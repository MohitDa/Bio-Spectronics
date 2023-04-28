BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Tests" (
	"primary_key"	INTEGER NOT NULL,
	"test_name"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"temp"	INTEGER NOT NULL,
	"wavelength"	INTEGER NOT NULL,
	"unit"	TEXT NOT NULL,
	"result_low"	INTEGER NOT NULL,
	"result_high"	INTEGER NOT NULL,
	"sample_rest_time"	INTEGER NOT NULL,
	"test_time"	INTEGER NOT NULL,
	"delay_between_images"	INTEGER NOT NULL,
	"standard_concentration"	INTEGER NOT NULL,
	"m"	INTEGER NOT NULL,
	"i"	INTEGER NOT NULL,
	PRIMARY KEY("primary_key")
);
INSERT INTO "Tests" VALUES (0,'Albumin','EP',37,630,'g/dl',0,0,0,0,0,4,0,0);
INSERT INTO "Tests" VALUES (1,'Alkaline Phosphatase','Kinatic',37,405,'IU/L',0,0,0,0,0,2754,0,0);
INSERT INTO "Tests" VALUES (2,'Alpha Amylase','Kinatic',37,405,'IU/L',0,0,0,0,0,4640,0,0);
INSERT INTO "Tests" VALUES (3,'Biliruin (T&D)','EP',37,546,'mg/dl',0,0,0,0,0,0,26.3,0);
INSERT INTO "Tests" VALUES (4,'Calcium','EP',27,630,'mg/dl',0,0,0,0,0,10,0,0);
INSERT INTO "Tests" VALUES (5,'Chloride','EP',37,505,'mmol/l',0,0,0,0,0,100,0,0);
INSERT INTO "Tests" VALUES (6,'Creatinine','TP',37,520,'mg/dl',0,0,0,0,0,2,0,0);
INSERT INTO "Tests" VALUES (7,'Cholesterol','EP',37,505,'mg/dl',0,0,0,0,0,200,0,0);
INSERT INTO "Tests" VALUES (8,'Glucose','EP',37,505,'mg/dl',0,0,0,0,0,100,0,0);
INSERT INTO "Tests" VALUES (9,'Hemoglobin','EP',37,540,'g/dl',0,0,0,0,0,60,0,0);
INSERT INTO "Tests" VALUES (10,'Sodium','EP',27,630,'mmol/l',0,0,0,0,0,150,0,0);
INSERT INTO "Tests" VALUES (11,'Potassium','EP',27,620,'mmol/l',0,0,0,0,0,5,0,0);
INSERT INTO "Tests" VALUES (12,'Phosphorous','EP',27,680,'mg/dl',0,0,0,0,0,5,0,0);
INSERT INTO "Tests" VALUES (13,'SGOT','Kinatic',37,340,'IU/L',0,0,0,0,0,0,1746,0);
INSERT INTO "Tests" VALUES (14,'SGPT','Kinatic',37,340,'IU/L',0,0,0,0,0,0,1746,0);
INSERT INTO "Tests" VALUES (15,'Total Protein','EP',37,555,'g/dl',0,0,0,0,0,6,0,0);
INSERT INTO "Tests" VALUES (16,'Tri Glycerides','EP',37,505,'mgdl',0,0,0,0,0,200,0,0);
COMMIT;
