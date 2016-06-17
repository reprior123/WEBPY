BEGIN TRANSACTION;
CREATE TABLE ISIN(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ISIN CHAR(512),
    Productname CHAR(512),
    symbol TEXT,
    type TEXT,
    AssetClass TEXT,
    Geography TEXT,
    Sector TEXT,
    Style TEXT,
    StkExch TEXT,
    Currency TEXT,
    priceEOD TEXT,
    pricePrevClose TEXT,
    priceOpen TEXT,
    FundInfodocflag TEXT,
    BidAsk TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE ISINs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    url CHAR(512),
    address CHAR(512),
    phone CHAR(512),
    fax CHAR(512),
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
, isin CHAR(512));
CREATE TABLE Trades(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    tradeprice TEXT,
    buysell TEXT,
    tradedate TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE auth_cas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP,
    service CHAR(512),
    ticket CHAR(512),
    renew CHAR(1)
);
CREATE TABLE auth_event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_stamp TIMESTAMP,
    client_ip CHAR(512),
    user_id INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    origin CHAR(512),
    description TEXT
);
INSERT INTO "auth_event" VALUES(1,'2016-04-05 11:27:05','127.0.0.1',NULL,'auth','Group 1 created');
INSERT INTO "auth_event" VALUES(2,'2016-04-05 11:27:05','127.0.0.1',1,'auth','User 1 Registered');
INSERT INTO "auth_event" VALUES(3,'2016-04-06 13:27:54','127.0.0.1',NULL,'auth','Group 2 created');
INSERT INTO "auth_event" VALUES(4,'2016-04-06 13:27:54','127.0.0.1',2,'auth','User 2 Registered');
INSERT INTO "auth_event" VALUES(5,'2016-04-07 01:36:02','127.0.0.1',NULL,'auth','Group 3 created');
INSERT INTO "auth_event" VALUES(6,'2016-04-07 01:36:02','127.0.0.1',3,'auth','User 3 Registered');
INSERT INTO "auth_event" VALUES(7,'2016-04-15 13:49:40','127.0.0.1',NULL,'auth','Group 4 created');
INSERT INTO "auth_event" VALUES(8,'2016-04-15 13:49:40','127.0.0.1',4,'auth','User 4 Registered');
INSERT INTO "auth_event" VALUES(9,'2016-04-15 14:22:21','127.0.0.1',4,'auth','User 4 Logged-out');
INSERT INTO "auth_event" VALUES(10,'2016-04-15 14:22:38','127.0.0.1',4,'auth','User 4 Logged-in');
INSERT INTO "auth_event" VALUES(11,'2016-04-15 14:25:43','127.0.0.1',4,'auth','User 4 Logged-out');
INSERT INTO "auth_event" VALUES(12,'2016-04-15 14:26:30','127.0.0.1',4,'auth','User 4 Logged-in');
INSERT INTO "auth_event" VALUES(13,'2016-04-15 20:27:50','127.0.0.1',4,'auth','User 4 Logged-in');
CREATE TABLE auth_group(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role CHAR(512),
    description TEXT
);
INSERT INTO "auth_group" VALUES(1,'user_1','Group uniquely assigned to user 1');
INSERT INTO "auth_group" VALUES(2,'user_2','Group uniquely assigned to user 2');
INSERT INTO "auth_group" VALUES(3,'user_3','Group uniquely assigned to user 3');
INSERT INTO "auth_group" VALUES(4,'user_4','Group uniquely assigned to user 4');
CREATE TABLE auth_membership(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    group_id INTEGER REFERENCES auth_group (id) ON DELETE CASCADE  
);
INSERT INTO "auth_membership" VALUES(1,1,1);
INSERT INTO "auth_membership" VALUES(2,2,2);
INSERT INTO "auth_membership" VALUES(3,3,3);
INSERT INTO "auth_membership" VALUES(4,4,4);
CREATE TABLE auth_permission(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER REFERENCES auth_group (id) ON DELETE CASCADE  ,
    name CHAR(512),
    table_name CHAR(512),
    record_id INTEGER
);
CREATE TABLE auth_user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name CHAR(128),
    last_name CHAR(128),
    email CHAR(512),
    password CHAR(512),
    registration_key CHAR(512),
    reset_password_key CHAR(512),
    registration_id CHAR(512)
);
INSERT INTO "auth_user" VALUES(1,'rob','p','rp@bal.com','sha512$8520c53cac7290f0$57aa29508bdb4d9748161a6bf6508bcd324044cfcf45518c8f80c20b2f0d7ba7d1f3f38c33fee2967493e003408441383f1ad22e498881fa5848255298df77f2','','','');
INSERT INTO "auth_user" VALUES(2,'rob','rob','rr@r.com','sha512$8da2083014f09b7c$269392ef6f11be026de0b3e093d54075d06513b351724b5a98310bd16913ab0bef1e93b64431d788db338d0a74cc20bd04bb0053a5a1ca7c8f0a8598066470ba','','','');
INSERT INTO "auth_user" VALUES(3,'rob','r','rr@rr.com','sha512$b95a71617097bd71$c56c12aa01d14fc0295bfa1e89063fa57d1175704bc731e543efc7afe815ba8b47549e28bbb0f3ae3d71d61398116a612ab41701a1e5c87e49c294c149627013','','','');
INSERT INTO "auth_user" VALUES(4,'rob','whatismyidnum','reprior123@gmail.com','sha512$919d74e0d3d2fe34$2480ee4ccb5ae3da84e6c6610a7622628530fb6141929c0eabfbfd3a44534a3ba4407131025ca4c31f2fa1ad47684c4c50404e5a563acfd453e2d01db4de5f48','','','');
CREATE TABLE company(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    url CHAR(512),
    address CHAR(512),
    phone CHAR(512),
    fax CHAR(512),
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
INSERT INTO "company" VALUES(1,'newco3','http://url@dd.com','addre','123','123',4,'2016-04-15 14:46:04');
INSERT INTO "company" VALUES(2,'newco4','','','','',4,'2016-04-15 14:47:53');
CREATE TABLE document(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person INTEGER REFERENCES person (id) ON DELETE CASCADE  ,
    name CHAR(512),
    file CHAR(512),
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person INTEGER REFERENCES person (id) ON DELETE CASCADE  ,
    body TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE person(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    company INTEGER REFERENCES company (id) ON DELETE CASCADE  ,
    role CHAR(512),
    address CHAR(512),
    phone CHAR(512),
    fax CHAR(512),
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
, firstname CHAR(512), lastname CHAR(512));
CREATE TABLE personew(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name CHAR(512),
    first_name CHAR(512)
);
CREATE TABLE personnew(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name CHAR(512),
    first_name CHAR(512)
);
INSERT INTO "personnew" VALUES(1,'Smith0','John0');
INSERT INTO "personnew" VALUES(2,'Smith1','John1');
INSERT INTO "personnew" VALUES(3,'Smith2','John2');
INSERT INTO "personnew" VALUES(4,'Smith3','John3');
INSERT INTO "personnew" VALUES(5,'Smith4','John4');
INSERT INTO "personnew" VALUES(6,'Smith5','John5');
INSERT INTO "personnew" VALUES(7,'Smith6','John6');
INSERT INTO "personnew" VALUES(8,'Smith7','John7');
INSERT INTO "personnew" VALUES(9,'Smith8','John8');
INSERT INTO "personnew" VALUES(10,'Smith9','John9');
INSERT INTO "personnew" VALUES(11,'Smith10','John10');
INSERT INTO "personnew" VALUES(12,'Smith11','John11');
INSERT INTO "personnew" VALUES(13,'Smith12','John12');
INSERT INTO "personnew" VALUES(14,'Smith13','John13');
INSERT INTO "personnew" VALUES(15,'Smith14','John14');
INSERT INTO "personnew" VALUES(16,'Smith15','John15');
INSERT INTO "personnew" VALUES(17,'Smith16','John16');
INSERT INTO "personnew" VALUES(18,'Smith17','John17');
INSERT INTO "personnew" VALUES(19,'Smith18','John18');
INSERT INTO "personnew" VALUES(20,'Smith19','John19');
INSERT INTO "personnew" VALUES(21,'Smith20','John20');
INSERT INTO "personnew" VALUES(22,'Smith21','John21');
INSERT INTO "personnew" VALUES(23,'Smith22','John22');
INSERT INTO "personnew" VALUES(24,'Smith23','John23');
INSERT INTO "personnew" VALUES(25,'Smith24','John24');
INSERT INTO "personnew" VALUES(26,'Smith25','John25');
INSERT INTO "personnew" VALUES(27,'Smith26','John26');
INSERT INTO "personnew" VALUES(28,'Smith27','John27');
INSERT INTO "personnew" VALUES(29,'Smith28','John28');
INSERT INTO "personnew" VALUES(30,'Smith29','John29');
INSERT INTO "personnew" VALUES(31,'Smith30','John30');
INSERT INTO "personnew" VALUES(32,'Smith31','John31');
INSERT INTO "personnew" VALUES(33,'Smith32','John32');
INSERT INTO "personnew" VALUES(34,'Smith33','John33');
INSERT INTO "personnew" VALUES(35,'Smith34','John34');
INSERT INTO "personnew" VALUES(36,'Smith35','John35');
INSERT INTO "personnew" VALUES(37,'Smith36','John36');
INSERT INTO "personnew" VALUES(38,'Smith37','John37');
INSERT INTO "personnew" VALUES(39,'Smith38','John38');
INSERT INTO "personnew" VALUES(40,'Smith39','John39');
INSERT INTO "personnew" VALUES(41,'Smith40','John40');
INSERT INTO "personnew" VALUES(42,'Smith41','John41');
INSERT INTO "personnew" VALUES(43,'Smith42','John42');
INSERT INTO "personnew" VALUES(44,'Smith43','John43');
INSERT INTO "personnew" VALUES(45,'Smith44','John44');
INSERT INTO "personnew" VALUES(46,'Smith45','John45');
INSERT INTO "personnew" VALUES(47,'Smith46','John46');
INSERT INTO "personnew" VALUES(48,'Smith47','John47');
INSERT INTO "personnew" VALUES(49,'Smith48','John48');
INSERT INTO "personnew" VALUES(50,'Smith49','John49');
INSERT INTO "personnew" VALUES(51,'Smith50','John50');
INSERT INTO "personnew" VALUES(52,'Smith51','John51');
INSERT INTO "personnew" VALUES(53,'Smith52','John52');
INSERT INTO "personnew" VALUES(54,'Smith53','John53');
INSERT INTO "personnew" VALUES(55,'Smith54','John54');
INSERT INTO "personnew" VALUES(56,'Smith55','John55');
INSERT INTO "personnew" VALUES(57,'Smith56','John56');
INSERT INTO "personnew" VALUES(58,'Smith57','John57');
INSERT INTO "personnew" VALUES(59,'Smith58','John58');
INSERT INTO "personnew" VALUES(60,'Smith59','John59');
INSERT INTO "personnew" VALUES(61,'Smith60','John60');
INSERT INTO "personnew" VALUES(62,'Smith61','John61');
INSERT INTO "personnew" VALUES(63,'Smith62','John62');
INSERT INTO "personnew" VALUES(64,'Smith63','John63');
INSERT INTO "personnew" VALUES(65,'Smith64','John64');
INSERT INTO "personnew" VALUES(66,'Smith65','John65');
INSERT INTO "personnew" VALUES(67,'Smith66','John66');
INSERT INTO "personnew" VALUES(68,'Smith67','John67');
INSERT INTO "personnew" VALUES(69,'Smith68','John68');
INSERT INTO "personnew" VALUES(70,'Smith69','John69');
INSERT INTO "personnew" VALUES(71,'Smith70','John70');
INSERT INTO "personnew" VALUES(72,'Smith71','John71');
INSERT INTO "personnew" VALUES(73,'Smith72','John72');
INSERT INTO "personnew" VALUES(74,'Smith73','John73');
INSERT INTO "personnew" VALUES(75,'Smith74','John74');
INSERT INTO "personnew" VALUES(76,'Smith75','John75');
INSERT INTO "personnew" VALUES(77,'Smith76','John76');
INSERT INTO "personnew" VALUES(78,'Smith77','John77');
INSERT INTO "personnew" VALUES(79,'Smith78','John78');
INSERT INTO "personnew" VALUES(80,'Smith79','John79');
INSERT INTO "personnew" VALUES(81,'Smith80','John80');
INSERT INTO "personnew" VALUES(82,'Smith81','John81');
INSERT INTO "personnew" VALUES(83,'Smith82','John82');
INSERT INTO "personnew" VALUES(84,'Smith83','John83');
INSERT INTO "personnew" VALUES(85,'Smith84','John84');
INSERT INTO "personnew" VALUES(86,'Smith85','John85');
INSERT INTO "personnew" VALUES(87,'Smith86','John86');
INSERT INTO "personnew" VALUES(88,'Smith87','John87');
INSERT INTO "personnew" VALUES(89,'Smith88','John88');
INSERT INTO "personnew" VALUES(90,'Smith89','John89');
INSERT INTO "personnew" VALUES(91,'Smith90','John90');
INSERT INTO "personnew" VALUES(92,'Smith91','John91');
INSERT INTO "personnew" VALUES(93,'Smith92','John92');
INSERT INTO "personnew" VALUES(94,'Smith93','John93');
INSERT INTO "personnew" VALUES(95,'Smith94','John94');
INSERT INTO "personnew" VALUES(96,'Smith95','John95');
INSERT INTO "personnew" VALUES(97,'Smith96','John96');
INSERT INTO "personnew" VALUES(98,'Smith97','John97');
INSERT INTO "personnew" VALUES(99,'Smith98','John98');
INSERT INTO "personnew" VALUES(100,'Smith99','John99');
INSERT INTO "personnew" VALUES(101,'Smith100','John100');
CREATE TABLE plugin_tagging_tag(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    counter INTEGER,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE plugin_tagging_tag_link(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag INTEGER REFERENCES plugin_tagging_tag (id) ON DELETE CASCADE  ,
    table_name CHAR(512),
    record_id INTEGER
);
CREATE TABLE portfddddolio(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    symbol TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE portfolio(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_name CHAR(512),
    category TEXT,
    type TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE portfolio_rp(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    symbol TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
, avgcostpershare TEXT, avgcost TEXT, position TEXT, portfolioname CHAR(512), portfoliogroup TEXT, company INTEGER REFERENCES company (id) ON DELETE CASCADE);
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    symbol TEXT,
    type TEXT,
    AssetClass TEXT,
    Geography TEXT,
    Sector TEXT,
    Style TEXT,
    StkExch TEXT,
    Currency TEXT,
    priceEOD TEXT,
    pricePrevClose TEXT,
    priceOpen TEXT,
    FundInfodocflag TEXT,
    BidAsk TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
CREATE TABLE products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    symbol TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
, sector TEXT, assetclass TEXT, priceeod TEXT, style TEXT, currency TEXT, priceopen TEXT, fundinfodocflag TEXT, stkexch TEXT, bidask TEXT, type TEXT, priceprevclose TEXT, geography TEXT);
CREATE TABLE productsport(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(512),
    isin TEXT,
    symbol TEXT,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('auth_user',4);
INSERT INTO "sqlite_sequence" VALUES('auth_group',4);
INSERT INTO "sqlite_sequence" VALUES('auth_event',13);
INSERT INTO "sqlite_sequence" VALUES('auth_membership',4);
INSERT INTO "sqlite_sequence" VALUES('personnew',101);
INSERT INTO "sqlite_sequence" VALUES('company',2);
CREATE TABLE task(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title CHAR(512),
    task_type CHAR(512),
    person INTEGER REFERENCES person (id) ON DELETE CASCADE  ,
    description TEXT,
    start_time TIMESTAMP,
    stop_time TIMESTAMP,
    created_by INTEGER REFERENCES auth_user (id) ON DELETE CASCADE  ,
    created_on TIMESTAMP
);
COMMIT;
