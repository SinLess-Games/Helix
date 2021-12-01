CREATE DATABASE Web_Permissions;

CREATE TABLE Web_User (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, 
    Real_Name VARCHAR(100),
    LogIn_ID VARCHAR(50),
    Login_Password VARCHAR(200), (encrypt)
    Security_Question_1 VARCHAR(50),
    Answer_1 VARCHAR(100),
    Security_Question_2 VARCHAR(50),
    Answer_2 VARCHAR(100),
    Security_Question_3 VARCHAR(50),
    Answer_3 VARCHAR(100),
    Email VARCHAR(100),
    discord_name VARCHAR(100),
    discord_token VARCHAR(100),
    discord_Client_secret VARCHAR(100),
    liscene_key VARCHAR(24),
    Permission_Groups VARCHAR(100), 
    Access_level BIGINT(10)
);

CREATE TABLE Permission_Groups (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, 
    Group_Name VARCHAR(50) UNIQUE,
    Invited VARCHAR(5),
    Invited_User_Group VARCHAR(5),
    Permissions BIGINT(20),
    User_Count BIGINT(5),
    Active_Status VARCHAR(8),
    Used_Unused VARCHAR(6)
);

CREATE TABLE Permissions (
    ID BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
    Permission_Name VARCHAR(100),
    Access VARCHAR(100),
    Users_With_Permission BIGINT(10),
    Used_Unused VARCHAR(6)
);