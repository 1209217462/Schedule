
create database schedule;
use schedule;
create table record (id integer, username varchar(255) not null ,  content varchar(255) not null,state integer not null,timing datetime not null , primary key (id));
create table user (id integer,user varchar(255) not null,password varchar(255) not null  ,primary key (id));
show tables;

