-- MySQL dump 10.13  Distrib 5.7.43, for Linux (x86_64)
--
-- Host: mysql-db    Database: cafehere-db
-- ------------------------------------------------------
-- Server version	5.7.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `cafehere-db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `cafehere-db` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cafehere-db`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authentication_user`
--

DROP TABLE IF EXISTS `authentication_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `uuid` char(32) NOT NULL,
  `mobile` varchar(18) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authentication_user_groups`
--

DROP TABLE IF EXISTS `authentication_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `authentication_user_groups_user_id_group_id_8af031ac_uniq` (`user_id`,`group_id`),
  KEY `authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id` (`group_id`),
  CONSTRAINT `authentication_user__user_id_30868577_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`),
  CONSTRAINT `authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authentication_user_user_permissions`
--

DROP TABLE IF EXISTS `authentication_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `authentication_user_user_user_id_permission_id_ec51b09f_uniq` (`user_id`,`permission_id`),
  KEY `authentication_user__permission_id_ea6be19a_fk_auth_perm` (`permission_id`),
  CONSTRAINT `authentication_user__permission_id_ea6be19a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `authentication_user__user_id_736ebf7e_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cafes_cafe`
--

DROP TABLE IF EXISTS `cafes_cafe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cafes_cafe` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `uuid` char(32) NOT NULL,
  `name` varchar(30) NOT NULL,
  `owner_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `unique_cafe_name_per_user` (`name`,`owner_id`),
  KEY `cafes_cafe_owner_id_97eebcc5_fk_authentication_user_id` (`owner_id`),
  CONSTRAINT `cafes_cafe_owner_id_97eebcc5_fk_authentication_user_id` FOREIGN KEY (`owner_id`) REFERENCES `authentication_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_authentication_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_authentication_user_id` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_category`
--

DROP TABLE IF EXISTS `products_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `cafe_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_category_per_cafe` (`name`,`cafe_id`),
  KEY `products_category_cafe_id_5de2403f_fk_cafes_cafe_id` (`cafe_id`),
  CONSTRAINT `products_category_cafe_id_5de2403f_fk_cafes_cafe_id` FOREIGN KEY (`cafe_id`) REFERENCES `cafes_cafe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_option`
--

DROP TABLE IF EXISTS `products_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_option` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `add_price` int(11) NOT NULL,
  `option_group_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_option_per_option_group` (`name`,`option_group_id`),
  KEY `products_option_option_group_id_0334e148_fk_products_` (`option_group_id`),
  CONSTRAINT `products_option_option_group_id_0334e148_fk_products_` FOREIGN KEY (`option_group_id`) REFERENCES `products_optiongroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_optiongroup`
--

DROP TABLE IF EXISTS `products_optiongroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_optiongroup` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `cafe_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_option_group_per_cafe` (`name`,`cafe_id`),
  KEY `products_optiongroup_cafe_id_2be5e49c_fk_cafes_cafe_id` (`cafe_id`),
  CONSTRAINT `products_optiongroup_cafe_id_2be5e49c_fk_cafes_cafe_id` FOREIGN KEY (`cafe_id`) REFERENCES `cafes_cafe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `cost` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `expireation_date` datetime(6) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `initial_consonant` varchar(30) NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_product_per_category` (`name`,`category_id`),
  KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`),
  CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_product_option_groups`
--

DROP TABLE IF EXISTS `products_product_option_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_product_option_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(20) NOT NULL,
  `optiongroup_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `products_product_option__product_id_optiongroup_i_f6de499f_uniq` (`product_id`,`optiongroup_id`),
  KEY `products_product_opt_optiongroup_id_d64e313c_fk_products_` (`optiongroup_id`),
  CONSTRAINT `products_product_opt_optiongroup_id_d64e313c_fk_products_` FOREIGN KEY (`optiongroup_id`) REFERENCES `products_optiongroup` (`id`),
  CONSTRAINT `products_product_opt_product_id_06f99916_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_authentic` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-02 14:51:44
