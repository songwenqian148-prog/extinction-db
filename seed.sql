-- ======================
-- 史前生物大灭绝 完整数据库脚本
-- 表：extinction_events / extinct_species / extinction_causes
-- ======================

-- 1. 创建三张关联数据表
CREATE TABLE IF NOT EXISTS extinction_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    start_ma REAL,
    end_ma REAL,
    brief_desc TEXT,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS extinct_species (
    species_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    species_name TEXT NOT NULL,
    taxon_group TEXT,
    source TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES extinction_events(event_id)
);

CREATE TABLE IF NOT EXISTS extinction_causes (
    cause_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    cause_type TEXT NOT NULL,
    description TEXT,
    source TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES extinction_events(event_id)
);

-- ======================
-- 2. 灭绝事件 extinction_events
-- ======================
INSERT INTO extinction_events(event_name,start_ma,end_ma,brief_desc,source)
VALUES
('奥陶纪末大灭绝',443.8,443.4,'全球气候变冷，海平面大幅下降，大量海洋底栖生物消失','Benton, M. J. (2015). Vertebrate Paleontology'),
('晚泥盆世大灭绝',359,358,'长期气候波动与海洋缺氧，珊瑚、盾皮鱼大量消亡','Palaeogeography, Palaeoclimatology, Palaeoecology'),
('二叠纪末大灭绝',252,251.9,'史上最严重灭绝事件，火山喷发导致温室效应，96%海洋生物灭绝','Nature 2018'),
('三叠纪末大灭绝',201.4,201.3,'大规模玄武岩火山喷发，温室气体快速增加，大量两栖类、合弓纲消失','Science Advances 2021'),
('白垩纪末大灭绝',66,66,'小行星撞击+火山活动，非鸟恐龙、菊石灭绝','Science 2010'),
('寒武纪灭绝事件',510,509,'海洋环境扰动，古杯动物、奥尔登三叶虫消失','The Geologic Time Scale 2012'),
('早奥陶世灭绝事件',478,477,'海盆缺氧，古杯海绵灭绝','Palaeogeography, Palaeoclimatology, Palaeoecology'),
('奥陶纪早期特马豆克灭绝',485,484,'早期海洋缺氧事件，大量浮游生物消亡','Palaeogeography, Palaeoclimatology, Palaeoecology 2022'),
('中奥陶世达尔文期灭绝',467,465,'区域海盆缺氧，腕足类、三叶虫多样性下降','Journal of the Geological Society 2020'),
('晚奥陶世库尔干事件',440,439,'冰川融化海平面快速上升，底栖群落崩溃','Earth-Science Reviews 2021'),
('早泥盆世普莱格尔灭绝',407,406,'气候冷暖波动，珊瑚礁生态受损','Palaeontology 2019'),
('中泥盆世吉维特期危机',388,387,'海洋富营养化，礁体生物大量减少','Global and Planetary Change 2023'),
('晚泥盆世弗拉斯-法门灭绝',372,371,'多次缺氧脉冲，珊瑚、层孔虫彻底衰落','Nature Communications 2020'),
('石炭纪晚期冰期生物危机',305,304,'冈瓦纳冰盖扩张，海平面震荡，海洋无脊椎动物衰减','Palaeogeography 2022'),
('早二叠世空谷期灭绝',280,279,'大规模火山活动，海水酸化，底栖生物减少','Geology 2021'),
('中二叠世瓜德鲁普末期灭绝',260,259,'峨眉山大火成岩省喷发，海洋缺氧','Science 2019'),
('晚三叠世瑞替期小型灭绝',208,207,'局部火山扰动，淡水两栖类衰退','Palaeontology 2022'),
('早侏罗世托阿尔大洋缺氧事件',183,182,'大规模火山喷发，全球广泛海洋缺氧','Earth-Science Reviews 2020'),
('中侏罗世卡洛期生物扰动',166,165,'气候变暖，海相无脊椎动物更替','Journal of Paleontology 2021'),
('晚侏罗世提塘期灭绝',152,151,'海平面下降，浅海礁生物衰退','Palaeogeography 2023'),
('早白垩世阿普特大洋缺氧事件',120,119,'火山释放温室气体，海洋缺氧与酸化','Nature Geoscience 2018'),
('中白垩世阿尔布期危机',105,104,'大洋缺氧，浮游有孔虫大量死亡','Geology 2022'),
('晚白垩世土仑期缺氧事件',94,93,'海平面上升，大陆边缘缺氧带扩张','Palaeogeography 2021'),
('晚白垩世康尼亚克期灭绝',86,85,'气候波动，菊石、双壳类多样性下降','Journal of Paleontology 2020');

-- ======================
-- 3. 灭绝物种 extinct_species
-- ======================
INSERT INTO extinct_species(event_id,species_name,taxon_group,source)
VALUES
(1,'Didymograptus','笔石','Benton, M. J. (2015)'),
(1,'Asaphus','三叶虫','Benton, M. J. (2015)'),
(1,'Cystoid','海林檎','Benton, M. J. (2015)'),
(1,'Triarthrus','三叶虫','Benton, M. J. (2015)'),
(1,'Glossograptus','笔石','Benton, M. J. (2015)'),
(2,'Dunkleosteus','盾皮鱼','Palaeogeography 2016'),
(2,'Manticoceras','菊石','Palaeogeography 2016'),
(2,'Stromatopora','层孔虫','Palaeogeography 2016'),
(2,'Coccosteus','盾皮鱼','Palaeogeography 2016'),
(2,'Actinostroma','层孔虫','Palaeogeography 2016'),
(3,'Lystrosaurus','水龙兽','Nature 2018'),
(3,'Paraceratites','菊石','Nature 2018'),
(3,'Calamites','芦木','Nature 2018'),
(3,'Proterosuchus','主龙形动物','Nature 2018'),
(3,'Pareiasaurus','锯齿龙','Nature 2018'),
(4,'Euparkeria','主龙类','Science Advances 2021'),
(4,'Metoposaurus','大型两栖类','Science Advances 2021'),
(4,'Phytosaur','植龙','Science Advances 2021'),
(4,'Rutiodon','植龙','Science Advances 2021'),
(4,'Gerrothorax','两栖类','Science Advances 2021'),
(5,'Tyrannosaurus rex','恐龙','Science 2010'),
(5,'Triceratops','恐龙','Science 2010'),
(5,'Baculites','菊石','Science 2010'),
(5,'Edmontosaurus','鸭嘴龙','Science 2010'),
(5,'Ankylosaurus','甲龙','Science 2010'),
(5,'Hesperornis','黄昏鸟','Science 2010'),
(6,'Olenellus','奥尔登三叶虫','The Geologic Time Scale 2012'),
(6,'Archaeocyathus','古杯动物','The Geologic Time Scale 2012'),
(6,'Redlichia','莱德利基三叶虫','The Geologic Time Scale 2012'),
(6,'Botomaella','古杯类','The Geologic Time Scale 2012'),
(7,'Archaeocyathid sponge','古杯海绵','Palaeogeography 2019'),
(7,'Siphonobolus','腕足类','Palaeogeography 2019'),
(7,'Dictyonema','网格笔石','Palaeogeography 2019'),
(8,'Agnostus','球接子三叶虫','Palaeogeography 2022'),
(8,'Siphonotreta','腕足动物','Palaeogeography 2022'),
(9,'Dalmanitina','三叶虫','Journal of the Geological Society 2020'),
(9,'Cyclopyge','三叶虫','Journal of the Geological Society 2020'),
(10,'Eurydice','介形虫','Earth-Science Reviews 2021'),
(10,'Chitinozoa','几丁虫','Earth-Science Reviews 2021'),
(11,'Pterygotus','板足鲎','Palaeontology 2019'),
(11,'Phacops','三叶虫','Palaeontology 2019'),
(12,'Hexagonaria','珊瑚','Global and Planetary Change 2023'),
(12,'Atrypa','腕足类','Global and Planetary Change 2023'),
(13,'Manticoceras','菊石','Nature Communications 2020'),
(13,'Prototaxites','巨型真菌','Nature Communications 2020'),
(14,'Productus','长身贝','Palaeogeography 2022'),
(14,'Fusulina','䗴类','Palaeogeography 2022'),
(15,'Stenopora','苔藓虫','Geology 2021'),
(15,'Neospirifer','腕足类','Geology 2021'),
(16,'Waagenites','腕足类','Science 2019'),
(16,'Codonofusiella','䗴类','Science 2019'),
(17,'Cyclotosaurus','大型离片椎两栖类','Palaeontology 2022'),
(17,'Mastodonsaurus','大型两栖类','Palaeontology 2022'),
(18,'Dactylioceras','菊石','Earth-Science Reviews 2020'),
(18,'Posidonia','双壳类','Earth-Science Reviews 2020'),
(19,'Perisphinctes','菊石','Journal of Paleontology 2021'),
(19,'Lithophaga','石蛏','Journal of Paleontology 2021'),
(20,'Himalayites','菊石','Palaeogeography 2023'),
(20,'Terebratula','穿孔贝','Palaeogeography 2023'),
(21,'Parahoplites','菊石','Nature Geoscience 2018'),
(21,'Schackoina','有孔虫','Nature Geoscience 2018'),
(22,'Mortoniceras','菊石','Geology 2022'),
(22,'Rotalipora','有孔虫','Geology 2022'),
(23,'Vascoceras','菊石','Palaeogeography 2021'),
(23,'Inoceramus','箭石','Palaeogeography 2021'),
(24,'Texanites','菊石','Journal of Paleontology 2020'),
(24,'Cremnoceramus','双壳类','Journal of Paleontology 2020');

-- ======================
-- 4. 灭绝诱因 extinction_causes
-- ======================
INSERT INTO extinction_causes(event_id,cause_type,description,source)
VALUES
(1,'全球降温','冈瓦纳大陆冰川扩张，海平面下降，浅海栖息地消失','Benton, M. J. (2015)'),
(2,'海洋缺氧','陆地植物演化带来大量营养输入，海水缺氧','Palaeogeography 2016'),
(3,'大型火山喷发','西伯利亚暗色岩喷发，大量CO₂释放，海洋酸化','Nature 2018'),
(4,'火山温室效应','中大西洋玄武岩喷发，全球升温，水循环紊乱','Science Advances 2021'),
(5,'天体撞击','希克苏鲁伯小行星撞击，尘埃遮蔽阳光，食物链崩溃','Science 2010'),
(6,'海平面波动','寒武纪海侵海退反复，底栖生物栖息地不稳定','The Geologic Time Scale 2012'),
(7,'海水缺氧','早奥陶世海盆缺氧事件，滤食性海绵大量死亡','Palaeogeography 2019'),
(8,'海洋缺氧','早期陆源营养输入，陆表海缺氧扩张','Palaeogeography, Palaeoclimatology, Palaeoecology 2022'),
(9,'海平面震荡','区域构造运动造成海退，浅海栖息地缩小','Journal of the Geological Society 2020'),
(10,'快速海侵','冰川消融，海水快速淹没大陆架，底栖群落无法适应','Earth-Science Reviews 2021'),
(11,'气候波动','冷暖交替，珊瑚礁生态系统持续压力','Palaeontology 2019'),
(12,'富营养化','陆地风化加强，海水富营养化，缺氧扩大','Global and Planetary Change 2023'),
(13,'多次缺氧脉冲','多轮海水缺氧事件叠加，礁生物连续灭绝','Nature Communications 2020'),
(14,'冰盖扩张','全球降温，海平面下降，海相生物栖息地缩减','Palaeogeography 2022'),
(15,'火山释放CO₂','大规模火山活动升温，海水酸化','Geology 2021'),
(16,'大型火山喷发','峨眉山火山释放巨量温室气体，海洋缺氧酸化','Science 2019'),
(17,'局部火山扰动','大陆火山喷发，淡水生态系统受毒素与升温冲击','Palaeontology 2022'),
(18,'大洋缺氧','火山释放CO₂，洋流停滞，大洋广泛缺氧','Earth-Science Reviews 2020'),
(19,'海平变化','板块运动引发海平面升降，浅海生物更替','Journal of Paleontology 2021'),
(20,'海退事件','海平面下降，礁体环境消失，造礁生物衰退','Palaeogeography 2023'),
(21,'温室升温','火山排放，全球变暖，大洋缺氧','Nature Geoscience 2018'),
(22,'大洋缺氧','中层水缺氧，浮游有孔虫大量死亡','Geology 2022'),
(23,'大陆边缘缺氧','海平面升高，缺氧水体覆盖大陆架','Palaeogeography 2021'),
(24,'气候不稳定','温室气候波动，菊石、双壳类生存压力增大','Journal of Paleontology 2020');
