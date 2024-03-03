-- 创建一个名叫users的表 id, username, password 三个字段 id是主键 username和password不能为空 id是自增的
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL
);