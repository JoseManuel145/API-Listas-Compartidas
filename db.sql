create database if not exists shopping_list;

use shopping_list;

CREATE TABLE IF NOT EXISTS shared_lists (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY,
    list_id CHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (list_id) REFERENCES shared_lists(id)
);