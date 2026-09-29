-- FIX UNTUK MYSQL 9.7 - JANGAN PAKE mysql_native_password LAGI
-- Pake caching_sha2_password (default MySQL 9)

USE mysql;

DROP USER IF EXISTS 'super_admin'@'%';
DROP USER IF EXISTS 'manager_bdg'@'%';
DROP USER IF EXISTS 'staff_cs01'@'%';
DROP USER IF EXISTS 'finance01'@'%';
DROP USER IF EXISTS 'mekanik01'@'%';
DROP USER IF EXISTS 'customer_app'@'%';

CREATE USER 'super_admin'@'%' IDENTIFIED WITH caching_sha2_password BY 'super123';
CREATE USER 'manager_bdg'@'%' IDENTIFIED WITH caching_sha2_password BY 'manager123';
CREATE USER 'staff_cs01'@'%' IDENTIFIED WITH caching_sha2_password BY 'staff123';
CREATE USER 'finance01'@'%' IDENTIFIED WITH caching_sha2_password BY 'finance123';
CREATE USER 'mekanik01'@'%' IDENTIFIED WITH caching_sha2_password BY 'mekanik123';
CREATE USER 'customer_app'@'%' IDENTIFIED WITH caching_sha2_password BY 'customer123';

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
SELECT 'FIX MYSQL 9 SELESAI - pake caching_sha2_password' AS info;
