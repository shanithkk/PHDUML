/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - phduml
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`phduml` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `phduml`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `b_id` int(11) NOT NULL AUTO_INCREMENT,
  `op_id` int(11) DEFAULT NULL,
  `u_id` int(11) DEFAULT NULL,
  `sts` varchar(50) DEFAULT NULL,
  `b_date` date DEFAULT NULL,
  PRIMARY KEY (`b_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`b_id`,`op_id`,`u_id`,`sts`,`b_date`) values (1,1,1,'pending','2019-12-12'),(2,3,1,'pending','2020-01-27'),(3,3,3,'reject','2020-01-28'),(4,3,3,'pending','2020-01-28'),(5,3,3,'confirm','2020-01-28'),(6,3,3,'confirm','2020-01-28'),(7,3,3,'reject','2020-01-28'),(8,3,4,'pending','2020-01-28');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `l_id` int(11) DEFAULT NULL,
  `sub` varchar(40) NOT NULL,
  `complaint` varchar(100) NOT NULL,
  `c_date` date DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`id`,`l_id`,`sub`,`complaint`,`c_date`,`reply`) values (1,1,'1','1','2005-01-23','1'),(2,2,'52','15','2020-01-23','wertygff'),(3,2,'34','33','2020-01-23','24'),(4,3,'54','45','2020-01-23','6544');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `dimg` varchar(1000) DEFAULT NULL,
  `dname` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `d_dob` date NOT NULL,
  `spec` varchar(50) NOT NULL,
  `dplace` varchar(50) DEFAULT NULL,
  `dist` varchar(50) DEFAULT NULL,
  `dphone` bigint(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `h_name` varchar(50) NOT NULL,
  `h_place` varchar(50) DEFAULT NULL,
  `h_post` varchar(50) DEFAULT NULL,
  `h_pin` varchar(50) DEFAULT NULL,
  `exp` varchar(50) DEFAULT NULL,
  `qualification` varchar(70) DEFAULT NULL,
  `sts` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`did`,`lid`,`dimg`,`dname`,`gender`,`d_dob`,`spec`,`dplace`,`dist`,`dphone`,`email`,`h_name`,`h_place`,`h_post`,`h_pin`,`exp`,`qualification`,`sts`) values (1,11,'jj.jpg','sha','Male','1995-09-29','heart','kalpetta','wayanad',987456321,'kkd3ff@mnjs','lj','ljj','dsdgfg','123456','ugg','mbbs,md,','Approve'),(2,12,'20200123-151320IMG_20180930_181318-01.jpeg','qwe','Male','1995-09-29','heart','kalpetta','wayanad',9876543210,'asdf@gmail.com','wims','clt','clt','673211','asd','mbbs,md,','Approve'),(3,13,'20200123-151916IMG_20180930_181318-01.jpeg','zxc','Male','1995-02-10','heart','kalpetta','wayanad',9876543210,'zxc@gmail.com','wims','clt','dsdgfg','123456','ugg','mbbs,md,','Reject');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `l_id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(50) NOT NULL,
  `pass` varchar(50) NOT NULL,
  `u_type` varchar(20) NOT NULL,
  PRIMARY KEY (`l_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`l_id`,`uname`,`pass`,`u_type`) values (1,'admin','admin','admin'),(2,'dd','123','user'),(3,'kkddff@mnjs','asd','user'),(11,'dd1','dd','doctor'),(12,'asdf@gmail.com','123','doctor'),(13,'zxc@gmail.com','456','block');

/*Table structure for table `opschedule` */

DROP TABLE IF EXISTS `opschedule`;

CREATE TABLE `opschedule` (
  `op_id` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `f_time` time NOT NULL,
  `t_time` time NOT NULL,
  PRIMARY KEY (`op_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `opschedule` */

insert  into `opschedule`(`op_id`,`did`,`date`,`f_time`,`t_time`) values (1,2,'2019-12-12','10:00:00','16:00:00'),(3,2,'2020-01-30','09:00:00','16:00:00'),(4,1,'2020-02-02','10:00:00','14:00:00');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) DEFAULT NULL,
  `lid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `rate` float DEFAULT NULL,
  `b_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`id`,`did`,`lid`,`date`,`rate`,`b_id`) values (1,3,11,'2009-09-29',3,NULL);

/*Table structure for table `trainingset` */

DROP TABLE IF EXISTS `trainingset`;

CREATE TABLE `trainingset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `file` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `trainingset` */

insert  into `trainingset`(`id`,`date`,`file`) values (1,'2020-01-22','20200122-131642s.txt'),(2,'2020-01-23','20200123-154103s.txt'),(3,'2020-01-23','20200123-154333IMG_20180930_181318-01.jpeg');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `img` varchar(1000) DEFAULT NULL,
  `u_name` varchar(50) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `u_place` varchar(30) DEFAULT NULL,
  `u_dist` varchar(30) NOT NULL,
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`u_id`,`lid`,`img`,`u_name`,`age`,`ph_no`,`email`,`gender`,`u_place`,`u_dist`) values (2,2,'20200121-135920DSC_0108.JPG','shaniiiiii',24,987654321,'dd','Male','kalpett','Wayan'),(3,3,'20200122-110349DSC_0104.JPG','shanith',24,9876543210,'kkddff@mnjs','Male','kalpetta','Wayanad');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
