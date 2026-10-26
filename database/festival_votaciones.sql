-- Festival de Votaciones: estructura y datos de prueba (sin usuarios ni contraseñas).
-- Uso: mysql -u root -p festival_votaciones < database/festival_votaciones.sql
SET FOREIGN_KEY_CHECKS=0;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `votaciones_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `votaciones_categoria` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` longtext NOT NULL,
  `orden` smallint(5) unsigned NOT NULL CHECK (`orden` >= 0),
  `edicion_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `categoria_unica_por_edicion` (`edicion_id`,`nombre`),
  CONSTRAINT `votaciones_categoria_edicion_id_083fc430_fk_votacione` FOREIGN KEY (`edicion_id`) REFERENCES `votaciones_edicion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `votaciones_edicion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `votaciones_edicion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `anio` int(10) unsigned NOT NULL CHECK (`anio` >= 0),
  `nombre` varchar(150) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `activa` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `anio` (`anio`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `votaciones_opcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `votaciones_opcion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `orden` smallint(5) unsigned NOT NULL CHECK (`orden` >= 0),
  `activa` tinyint(1) NOT NULL,
  `votacion_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opcion_unica_por_votacion` (`votacion_id`,`nombre`),
  CONSTRAINT `votaciones_opcion_votacion_id_1aa9bd68_fk_votaciones_votacion_id` FOREIGN KEY (`votacion_id`) REFERENCES `votaciones_votacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `votaciones_votacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `votaciones_votacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_apertura` datetime(6) NOT NULL,
  `fecha_cierre` datetime(6) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `votos_por_usuario` smallint(5) unsigned NOT NULL CHECK (`votos_por_usuario` >= 0),
  `categoria_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `votaciones_votacion_categoria_id_1945fb03_fk_votacione` (`categoria_id`),
  CONSTRAINT `votaciones_votacion_categoria_id_1945fb03_fk_votacione` FOREIGN KEY (`categoria_id`) REFERENCES `votaciones_categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-10-25 22:17:03.823942');
INSERT INTO `django_migrations` VALUES (2,'auth','0001_initial','2026-10-25 22:17:03.900027');
INSERT INTO `django_migrations` VALUES (3,'admin','0001_initial','2026-10-25 22:17:03.917195');
INSERT INTO `django_migrations` VALUES (4,'admin','0002_logentry_remove_auto_add','2026-10-25 22:17:03.920677');
INSERT INTO `django_migrations` VALUES (5,'admin','0003_logentry_add_action_flag_choices','2026-10-25 22:17:03.924551');
INSERT INTO `django_migrations` VALUES (6,'contenttypes','0002_remove_content_type_name','2026-10-25 22:17:03.950898');
INSERT INTO `django_migrations` VALUES (7,'auth','0002_alter_permission_name_max_length','2026-10-25 22:17:03.961244');
INSERT INTO `django_migrations` VALUES (8,'auth','0003_alter_user_email_max_length','2026-10-25 22:17:03.970378');
INSERT INTO `django_migrations` VALUES (9,'auth','0004_alter_user_username_opts','2026-10-25 22:17:03.974545');
INSERT INTO `django_migrations` VALUES (10,'auth','0005_alter_user_last_login_null','2026-10-25 22:17:03.984792');
INSERT INTO `django_migrations` VALUES (11,'auth','0006_require_contenttypes_0002','2026-10-25 22:17:03.985620');
INSERT INTO `django_migrations` VALUES (12,'auth','0007_alter_validators_add_error_messages','2026-10-25 22:17:03.989582');
INSERT INTO `django_migrations` VALUES (13,'auth','0008_alter_user_username_max_length','2026-10-25 22:17:03.998255');
INSERT INTO `django_migrations` VALUES (14,'auth','0009_alter_user_last_name_max_length','2026-10-25 22:17:04.005848');
INSERT INTO `django_migrations` VALUES (15,'auth','0010_alter_group_name_max_length','2026-10-25 22:17:04.013755');
INSERT INTO `django_migrations` VALUES (16,'auth','0011_update_proxy_permissions','2026-10-25 22:17:04.023293');
INSERT INTO `django_migrations` VALUES (17,'auth','0012_alter_user_first_name_max_length','2026-10-25 22:17:04.031941');
INSERT INTO `django_migrations` VALUES (18,'sessions','0001_initial','2026-10-25 22:17:04.038976');
INSERT INTO `django_migrations` VALUES (19,'votaciones','0001_initial','2026-10-25 22:17:04.083420');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry');
INSERT INTO `django_content_type` VALUES (2,'auth','group');
INSERT INTO `django_content_type` VALUES (3,'auth','permission');
INSERT INTO `django_content_type` VALUES (4,'auth','user');
INSERT INTO `django_content_type` VALUES (5,'contenttypes','contenttype');
INSERT INTO `django_content_type` VALUES (6,'sessions','session');
INSERT INTO `django_content_type` VALUES (7,'votaciones','categoria');
INSERT INTO `django_content_type` VALUES (8,'votaciones','edicion');
INSERT INTO `django_content_type` VALUES (9,'votaciones','opcion');
INSERT INTO `django_content_type` VALUES (10,'votaciones','votacion');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry');
INSERT INTO `auth_permission` VALUES (2,'Can change log entry',1,'change_logentry');
INSERT INTO `auth_permission` VALUES (3,'Can delete log entry',1,'delete_logentry');
INSERT INTO `auth_permission` VALUES (4,'Can view log entry',1,'view_logentry');
INSERT INTO `auth_permission` VALUES (5,'Can add permission',3,'add_permission');
INSERT INTO `auth_permission` VALUES (6,'Can change permission',3,'change_permission');
INSERT INTO `auth_permission` VALUES (7,'Can delete permission',3,'delete_permission');
INSERT INTO `auth_permission` VALUES (8,'Can view permission',3,'view_permission');
INSERT INTO `auth_permission` VALUES (9,'Can add group',2,'add_group');
INSERT INTO `auth_permission` VALUES (10,'Can change group',2,'change_group');
INSERT INTO `auth_permission` VALUES (11,'Can delete group',2,'delete_group');
INSERT INTO `auth_permission` VALUES (12,'Can view group',2,'view_group');
INSERT INTO `auth_permission` VALUES (13,'Can add user',4,'add_user');
INSERT INTO `auth_permission` VALUES (14,'Can change user',4,'change_user');
INSERT INTO `auth_permission` VALUES (15,'Can delete user',4,'delete_user');
INSERT INTO `auth_permission` VALUES (16,'Can view user',4,'view_user');
INSERT INTO `auth_permission` VALUES (17,'Can add content type',5,'add_contenttype');
INSERT INTO `auth_permission` VALUES (18,'Can change content type',5,'change_contenttype');
INSERT INTO `auth_permission` VALUES (19,'Can delete content type',5,'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20,'Can view content type',5,'view_contenttype');
INSERT INTO `auth_permission` VALUES (21,'Can add session',6,'add_session');
INSERT INTO `auth_permission` VALUES (22,'Can change session',6,'change_session');
INSERT INTO `auth_permission` VALUES (23,'Can delete session',6,'delete_session');
INSERT INTO `auth_permission` VALUES (24,'Can view session',6,'view_session');
INSERT INTO `auth_permission` VALUES (25,'Can add edición',8,'add_edicion');
INSERT INTO `auth_permission` VALUES (26,'Can change edición',8,'change_edicion');
INSERT INTO `auth_permission` VALUES (27,'Can delete edición',8,'delete_edicion');
INSERT INTO `auth_permission` VALUES (28,'Can view edición',8,'view_edicion');
INSERT INTO `auth_permission` VALUES (29,'Can add categoría',7,'add_categoria');
INSERT INTO `auth_permission` VALUES (30,'Can change categoría',7,'change_categoria');
INSERT INTO `auth_permission` VALUES (31,'Can delete categoría',7,'delete_categoria');
INSERT INTO `auth_permission` VALUES (32,'Can view categoría',7,'view_categoria');
INSERT INTO `auth_permission` VALUES (33,'Can add votación',10,'add_votacion');
INSERT INTO `auth_permission` VALUES (34,'Can change votación',10,'change_votacion');
INSERT INTO `auth_permission` VALUES (35,'Can delete votación',10,'delete_votacion');
INSERT INTO `auth_permission` VALUES (36,'Can view votación',10,'view_votacion');
INSERT INTO `auth_permission` VALUES (37,'Can add opción',9,'add_opcion');
INSERT INTO `auth_permission` VALUES (38,'Can change opción',9,'change_opcion');
INSERT INTO `auth_permission` VALUES (39,'Can delete opción',9,'delete_opcion');
INSERT INTO `auth_permission` VALUES (40,'Can view opción',9,'view_opcion');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;

/*!40000 ALTER TABLE `votaciones_edicion` DISABLE KEYS */;
INSERT INTO `votaciones_edicion` VALUES (1,2025,'Festival 2025','Edición anterior del festival, ya cerrada.','2025-11-01','2025-11-30',0);
INSERT INTO `votaciones_edicion` VALUES (2,2026,'Festival 2026','Edición actual: música, cine y arte digital.','2026-11-01','2026-11-30',1);
/*!40000 ALTER TABLE `votaciones_edicion` ENABLE KEYS */;

/*!40000 ALTER TABLE `votaciones_categoria` DISABLE KEYS */;
INSERT INTO `votaciones_categoria` VALUES (1,'Mejor Canción','Reconocimiento a la mejor canción del festival.',1,1);
INSERT INTO `votaciones_categoria` VALUES (2,'Mejor Cortometraje','Reconocimiento a la mejor cortometraje del festival.',2,1);
INSERT INTO `votaciones_categoria` VALUES (3,'Mejor Arte Digital','Reconocimiento a la mejor arte digital del festival.',3,1);
INSERT INTO `votaciones_categoria` VALUES (4,'Mejor Canción','Reconocimiento a la mejor canción del festival.',1,2);
INSERT INTO `votaciones_categoria` VALUES (5,'Mejor Cortometraje','Reconocimiento a la mejor cortometraje del festival.',2,2);
INSERT INTO `votaciones_categoria` VALUES (6,'Mejor Arte Digital','Reconocimiento a la mejor arte digital del festival.',3,2);
/*!40000 ALTER TABLE `votaciones_categoria` ENABLE KEYS */;

/*!40000 ALTER TABLE `votaciones_votacion` DISABLE KEYS */;
INSERT INTO `votaciones_votacion` VALUES (1,'Votación Mejor Canción 2025','Elige tu favorito en Mejor Canción para la edición 2025.','2025-09-20 22:17:04.425093','2025-10-20 22:17:04.425093','cerrada',1,1);
INSERT INTO `votaciones_votacion` VALUES (2,'Votación Mejor Cortometraje 2025','Elige tu favorito en Mejor Cortometraje para la edición 2025.','2025-09-20 22:17:04.425093','2025-10-20 22:17:04.425093','cerrada',1,2);
INSERT INTO `votaciones_votacion` VALUES (3,'Votación Mejor Arte Digital 2025','Elige tu favorito en Mejor Arte Digital para la edición 2025.','2025-09-20 22:17:04.425093','2025-10-20 22:17:04.425093','cerrada',1,3);
INSERT INTO `votaciones_votacion` VALUES (4,'Votación Mejor Canción 2026','Elige tu favorito en Mejor Canción para la edición 2026.','2026-10-24 22:17:04.425093','2026-11-14 22:17:04.425093','abierta',1,4);
INSERT INTO `votaciones_votacion` VALUES (5,'Votación Mejor Cortometraje 2026','Elige tu favorito en Mejor Cortometraje para la edición 2026.','2026-10-24 22:17:04.425093','2026-11-14 22:17:04.425093','abierta',1,5);
INSERT INTO `votaciones_votacion` VALUES (6,'Votación Mejor Arte Digital 2026','Elige tu favorito en Mejor Arte Digital para la edición 2026.','2026-10-24 22:17:04.425093','2026-11-14 22:17:04.425093','abierta',1,6);
/*!40000 ALTER TABLE `votaciones_votacion` ENABLE KEYS */;

/*!40000 ALTER TABLE `votaciones_opcion` DISABLE KEYS */;
INSERT INTO `votaciones_opcion` VALUES (1,'Noches de Neón','Propuesta participante: Noches de Neón.',1,1,1);
INSERT INTO `votaciones_opcion` VALUES (2,'Río Abajo','Propuesta participante: Río Abajo.',2,1,1);
INSERT INTO `votaciones_opcion` VALUES (3,'Semilla de Sol','Propuesta participante: Semilla de Sol.',3,1,1);
INSERT INTO `votaciones_opcion` VALUES (4,'Eco Urbano','Propuesta participante: Eco Urbano.',4,1,1);
INSERT INTO `votaciones_opcion` VALUES (5,'La Última Estación','Propuesta participante: La Última Estación.',1,1,2);
INSERT INTO `votaciones_opcion` VALUES (6,'Papel y Tinta','Propuesta participante: Papel y Tinta.',2,1,2);
INSERT INTO `votaciones_opcion` VALUES (7,'Marea Alta','Propuesta participante: Marea Alta.',3,1,2);
INSERT INTO `votaciones_opcion` VALUES (8,'Ciudad Líquida','Propuesta participante: Ciudad Líquida.',1,1,3);
INSERT INTO `votaciones_opcion` VALUES (9,'Bosque de Píxeles','Propuesta participante: Bosque de Píxeles.',2,1,3);
INSERT INTO `votaciones_opcion` VALUES (10,'Aurora Binaria','Propuesta participante: Aurora Binaria.',3,1,3);
INSERT INTO `votaciones_opcion` VALUES (11,'Noches de Neón','Propuesta participante: Noches de Neón.',1,1,4);
INSERT INTO `votaciones_opcion` VALUES (12,'Río Abajo','Propuesta participante: Río Abajo.',2,1,4);
INSERT INTO `votaciones_opcion` VALUES (13,'Semilla de Sol','Propuesta participante: Semilla de Sol.',3,1,4);
INSERT INTO `votaciones_opcion` VALUES (14,'Eco Urbano','Propuesta participante: Eco Urbano.',4,1,4);
INSERT INTO `votaciones_opcion` VALUES (15,'La Última Estación','Propuesta participante: La Última Estación.',1,1,5);
INSERT INTO `votaciones_opcion` VALUES (16,'Papel y Tinta','Propuesta participante: Papel y Tinta.',2,1,5);
INSERT INTO `votaciones_opcion` VALUES (17,'Marea Alta','Propuesta participante: Marea Alta.',3,1,5);
INSERT INTO `votaciones_opcion` VALUES (18,'Ciudad Líquida','Propuesta participante: Ciudad Líquida.',1,1,6);
INSERT INTO `votaciones_opcion` VALUES (19,'Bosque de Píxeles','Propuesta participante: Bosque de Píxeles.',2,1,6);
INSERT INTO `votaciones_opcion` VALUES (20,'Aurora Binaria','Propuesta participante: Aurora Binaria.',3,1,6);
/*!40000 ALTER TABLE `votaciones_opcion` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

SET FOREIGN_KEY_CHECKS=1;
