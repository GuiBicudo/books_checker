-- Active: 1739398248604@@127.0.0.1@3306@books_proj
CREATE DATABASE books_proj;

CREATE TABLE usuarios (
    id INT auto_increment PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ra VARCHAR(100) NOT NULL
);

ALTER TABLE usuarios DROP COLUMN ra;

ALTER TABLE usuarios ADD COLUMN ra BIGINT not NULL;

CREATE TABLE livros (
    id INT auto_increment PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dia date NOT NULL
);

ALTER TABLE livros DROP COLUMN dia;

ALTER TABLE livros ADD COLUMN Quantidade INT not NULL;

ALTER TABLE livros DROP COLUMN nome;

ALTER TABLE livros ADD COLUMN nome_livro INT not NULL;

ALTER TABLE livros DROP COLUMN Quantidade;

ALTER TABLE livros ADD COLUMN quant_livro INT not NULL;

ALTER TABLE livros MODIFY nome_livro VARCHAR(255) not NULL;

CREATE TABLE alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('Aluno', 'Professor') NOT NULL
);

ALTER TABLE alunos ADD COLUMN ra INT;

DROP TABLE IF EXISTS usuarios;

DESCRIBE alunos;

CREATE TABLE forum_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES alunos(id)
);
CREATE TABLE forum_comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    text TEXT NOT NULL
);

ALTER TABLE forum_comments
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE forum_comments
ADD FOREIGN KEY (post_id) REFERENCES forum_posts(id);

ALTER TABLE forum_comments
ADD FOREIGN KEY (user_id) REFERENCES alunos(id);