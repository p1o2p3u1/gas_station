CREATE DATABASE IF NOT EXISTS pytrace default character set utf8 COLLATE utf8_general_ci;

use pytrace;

drop table if exists diff;
create table if not exists diff (
    id bigint not null AUTO_INCREMENT,
    filename varchar(255) not null,
    pre_version int not null,
    cur_version int not null,
    diff varchar(5000),
    primary key (id),
    unique key (filename, pre_version, cur_version)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;

drop table if exists file;
create table if not exists file (
    id bigint not null auto_increment,
    filename varchar(255) not null,
    version int not null,
    source longtext,
    primary key (id),
    unique key (filename, version)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;

drop table if exists dirs;
create table if not exists dirs(
    id bigint not null auto_increment,
    server varchar(100) not null,
    path varchar(255) not null,
    version int not null,
    dirs longtext not null,
    primary key(id),
    unique key(server, path, version)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;

drop table if exists job;
create table if not exists job(
    id bigint not null auto_increment,
    time datetime not null,
    username varchar(100) not null,
    userid varchar(100) not null,
    jobname varchar(255),
    primary key (id),
    index (userid, jobname)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

drop table if exists report;
create table if not exists report (
    id bigint not null auto_increment,
    job_id bigint not null,
    filename varchar(255) not null,
    version int not null,
    source longtext,
    line text,
    exec text,
    miss text,
    cov_result float,
    primary key (id),
    index (job_id)
)ENGINE=InnoDB  DEFAULT CHARSET=utf8;