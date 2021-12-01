CREATE DATABASE AI_Train_DataSet;

CREATE TABLE Voice_Commands (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Command VARCHAR(50),
    Script VARCHAR(100), (FILENAME)
    use_Discription VARCHAR(500),
    Association VARCHAR(50),
    AI_Target VARCHAR(50)
);
