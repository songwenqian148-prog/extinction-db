CREATE TABLE extinction_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT, -- 地质年代，例如：奥陶纪末期，约4.43亿年前
  fact TEXT, -- 灭绝事件史实描述
  names TEXT, -- 相关物种、研究学者名称
  places TEXT, -- 化石/地层发现地点
  source TEXT -- 原始资料来源（论文、权威古生物资料库名称）
);
