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

