-- ==========================================
-- FIX FINAL UNTUK MARIADB / XAMPP
-- Untuk temen yang pake MariaDB, bukan MySQL 9
-- ==========================================
USE rentalpinjam;

DROP USER IF EXISTS 'super_admin'@'%';
DROP USER IF EXISTS 'manager_bdg'@'%';
DROP USER IF EXISTS 'staff_cs01'@'%';
DROP USER IF EXISTS 'finance01'@'%';
DROP USER IF EXISTS 'mekanik01'@'%';
DROP USER IF EXISTS 'customer_app'@'%';

-- MariaDB pake mysql_native_password, BUKAN caching_sha2_password
CREATE USER 'super_admin'@'%' IDENTIFIED BY 'super123';
CREATE USER 'manager_bdg'@'%' IDENTIFIED BY 'manager123';
CREATE USER 'staff_cs01'@'%' IDENTIFIED BY 'staff123';
CREATE USER 'finance01'@'%' IDENTIFIED BY 'finance123';
CREATE USER 'mekanik01'@'%' IDENTIFIED BY 'mekanik123';
CREATE USER 'customer_app'@'%' IDENTIFIED BY 'customer123';

GRANT ALL PRIVILEGES ON rentalpinjam.* TO 'super_admin'@'%';

GRANT SELECT ON rentalpinjam.cabang TO 'manager_bdg'@'%';
GRANT SELECT, INSERT, UPDATE ON rentalpinjam.pegawai TO 'manager_bdg'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON rentalpinjam.penyewaan TO 'manager_bdg'@'%';
GRANT SELECT, INSERT, UPDATE ON rentalpinjam.pembayaran TO 'manager_bdg'@'%';
GRANT SELECT, INSERT, UPDATE ON rentalpinjam.kendaraan TO 'manager_bdg'@'%';
GRANT SELECT ON rentalpinjam.pelanggan TO 'manager_bdg'@'%';
GRANT SELECT ON rentalpinjam.member TO 'manager_bdg'@'%';
GRANT SELECT ON rentalpinjam.gps_log TO 'manager_bdg'@'%';

GRANT SELECT ON rentalpinjam.cabang TO 'staff_cs01'@'%';
GRANT SELECT ON rentalpinjam.kendaraan TO 'staff_cs01'@'%';
GRANT SELECT, INSERT, UPDATE ON rentalpinjam.pelanggan TO 'staff_cs01'@'%';
GRANT SELECT, INSERT, UPDATE ON rentalpinjam.penyewaan TO 'staff_cs01'@'%';
GRANT SELECT, INSERT ON rentalpinjam.pembayaran TO 'staff_cs01'@'%';
GRANT SELECT ON rentalpinjam.member TO 'staff_cs01'@'%';

GRANT SELECT ON rentalpinjam.cabang TO 'finance01'@'%';
GRANT SELECT ON rentalpinjam.penyewaan TO 'finance01'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON rentalpinjam.pembayaran TO 'finance01'@'%';
GRANT SELECT ON rentalpinjam.pelanggan TO 'finance01'@'%';
GRANT SELECT ON rentalpinjam.member TO 'finance01'@'%';

GRANT SELECT, UPDATE ON rentalpinjam.kendaraan TO 'mekanik01'@'%';
GRANT SELECT, INSERT ON rentalpinjam.gps_log TO 'mekanik01'@'%';
GRANT SELECT ON rentalpinjam.cabang TO 'mekanik01'@'%';

GRANT SELECT ON rentalpinjam.cabang TO 'customer_app'@'%';
GRANT SELECT ON rentalpinjam.kendaraan TO 'customer_app'@'%';

FLUSH PRIVILEGES;

SELECT 'FIX MARIADB SELESAI - siap pake di XAMPP / phpMyAdmin' AS info;
