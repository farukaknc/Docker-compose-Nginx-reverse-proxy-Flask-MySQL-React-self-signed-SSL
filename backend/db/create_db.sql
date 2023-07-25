DROP DATABASE IF EXISTS quizapp;
CREATE DATABASE quizapp;
USE quizapp;

CREATE TABLE IF NOT EXISTS Questions (
    Question_ID INT NOT NULL AUTO_INCREMENT,
    Course_Name VARCHAR(256) NOT NULL,
    Question_Desc VARCHAR(1000) NOT NULL,
    Choice1 VARCHAR(1000) NOT NULL,
    Choice2 VARCHAR(1000) NOT NULL,
    Choice3 VARCHAR(1000) NOT NULL,
    Choice4 VARCHAR(1000) NOT NULL,
    Choice5 VARCHAR(1000),
    Choice6 VARCHAR(1000),
    Correct_Answer VARCHAR(1000) NOT NULL,
    Question_Score FLOAT NOT NULL,
    Added_Datetime DATETIME,
    PRIMARY KEY (Question_ID)
) ENGINE=InnoDB AUTO_INCREMENT=1000;

INSERT INTO Questions (
    Course_Name, Question_Desc, Choice1, Choice2, Choice3, Choice4, Choice5, Choice6, Correct_Answer, Question_Score, Added_Datetime
) VALUES
    ('Empirical Research 1', 'Which of the following is NOT a type of research design commonly used in empirical research?',
    'Experimental', 'Narrative', 'Correlational', 'Descriptive', '', '', 'Narrative', 25.0, NOW()),
    ('Empirical Research 1', 'What is the primary goal of a pilot study in empirical research?',
    'To test the effectiveness of a new treatment', 'To determine the sample size needed for a larger study',
    'To identify potential confounding variables', 'To establish the reliability and validity of a measure', '', '',
    'To establish the reliability and validity of a measure', 25.0, NOW()),
    ('Empirical Research 1', 'What is the difference between internal and external validity in empirical research?',
    'Internal validity refers to the extent to which a study measures what it intends to measure, while external validity refers to the generalizability of the study''s findings to other populations or settings.',
    'Internal validity refers to the generalizability of the study''s findings to other populations or settings, while external validity refers to the extent to which a study measures what it intends to measure.',
    'Internal validity refers to the accuracy of a study''s findings, while external validity refers to the precision of a study''s measurements.',
    'Internal validity refers to the reproducibility of a study''s findings, while external validity refers to the generalizability of a study''s findings.', '', '',
    'Internal validity refers to the extent to which a study measures what it intends to measure, while external validity refers to the generalizability of the study''s findings to other populations or settings.', 25.0, NOW()),
    ('Empirical Research 1', 'A researcher wants to determine the effectiveness of a new reading program for children with dyslexia. Which research design would be most appropriate?',
    'Case study', 'Descriptive', 'Randomized controlled trial', 'Correlational', '', '', 'Randomized controlled trial', 25.0, NOW());

CREATE TABLE IF NOT EXISTS SelectedQuestions (
    Question_ID INT NOT NULL,
    Course_Name VARCHAR(256) NOT NULL,
    Question_Desc VARCHAR(1000) NOT NULL,
    Choice1 VARCHAR(1000) NOT NULL,
    Choice2 VARCHAR(1000) NOT NULL,
    Choice3 VARCHAR(1000) NOT NULL,
    Choice4 VARCHAR(1000) NOT NULL,
    Choice5 VARCHAR(1000),
    Choice6 VARCHAR(1000),
    Correct_Answer VARCHAR(1000) NOT NULL,
    Question_Score FLOAT NOT NULL,
    Added_Datetime DATETIME NOT NULL,
    Question_Number INT,
    QuizID INT,
    PRIMARY KEY (Question_ID)
);

CREATE TABLE IF NOT EXISTS QuizTable (
    QuizID INT NOT NULL AUTO_INCREMENT,
    Quiz_Datetime DATETIME NOT NULL,
    NumofParticipants INT,
    NumofQuestions INT NOT NULL,
    TotalScorePossible INT NOT NULL,
    Duration INT NOT NULL,
    Quiz_Status VARCHAR(50) NOT NULL,
    Quiz_Start_Time DATETIME NOT NULL,
    Quiz_End_Time DATETIME NOT NULL,
    PRIMARY KEY (QuizID)
) ENGINE=InnoDB AUTO_INCREMENT=1000;

CREATE TABLE IF NOT EXISTS UserLog (
    QuizID INT NOT NULL,
    Course_Name VARCHAR(256) NOT NULL,
    Question_ID INT NOT NULL,
    Student_Name VARCHAR(256) NOT NULL,
    StudentID INT NOT NULL,
    Question_Number INT NOT NULL,
    SelectedChoice VARCHAR(1000) NOT NULL,
    Correct_Answer VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS Results (
    QuizID INT NOT NULL,
    Student_Name VARCHAR(256) NOT NULL,
    StudentID INT NOT NULL,
    NumofQuestions INT NOT NULL,
    NumofQuestionsAnswered INT NOT NULL,
    TotalScore INT NOT NULL
);

DESCRIBE Questions;
DESCRIBE SelectedQuestions;
DESCRIBE QuizTable;
DESCRIBE UserLog;
DESCRIBE Results;
SHOW TABLES;
SELECT * FROM Questions;