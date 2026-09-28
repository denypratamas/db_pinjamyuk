-- Cleaned for MySQL 9.7.2 - rentalpinjam
-- Converted from MariaDB 10.4 dump
CREATE DATABASE IF NOT EXISTS `rentalpinjam` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `rentalpinjam`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

-- Struktur tabel `cabang`
DROP TABLE IF EXISTS `cabang`;
CREATE TABLE `cabang` (
  `ID_Cabang` varchar(50) NOT NULL,
  `Nama_Cabang` varchar(100) DEFAULT NULL,
  `Alamat` text DEFAULT NULL,
  `Nomor_Telepon` varchar(20) DEFAULT NULL,
  `Jumlah_Pegawai` int DEFAULT NULL,
  `Jumlah_Kendaraan_Tersedia` int DEFAULT NULL,
  PRIMARY KEY (`ID_Cabang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `pelanggan` (dibuat duluan karena direferensi banyak)
DROP TABLE IF EXISTS `pelanggan`;
CREATE TABLE `pelanggan` (
  `ID_Pelanggan` varchar(50) NOT NULL,
  `NIK` varchar(20) DEFAULT NULL,
  `Nama_Lengkap` varchar(100) DEFAULT NULL,
  `Alamat` text DEFAULT NULL,
  `No_HP` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Tanggal_Lahir` date DEFAULT NULL,
  `Jenis_Kelamin` varchar(20) DEFAULT NULL,
  `Status_Keanggotaan` varchar(50) DEFAULT NULL,
  `Status_Akun` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Pelanggan`),
  UNIQUE KEY `NIK` (`NIK`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `kendaraan`
DROP TABLE IF EXISTS `kendaraan`;
CREATE TABLE `kendaraan` (
  `ID_Kendaraan` varchar(50) NOT NULL,
  `Nomor_Polisi` varchar(20) DEFAULT NULL,
  `Merek` varchar(50) DEFAULT NULL,
  `Model` varchar(50) DEFAULT NULL,
  `Tahun_Pembuatan` int DEFAULT NULL,
  `Warna` varchar(30) DEFAULT NULL,
  `Kapasitas_Penumpang` int DEFAULT NULL,
  `Jenis_Kendaraan` varchar(50) DEFAULT NULL,
  `Transmisi` varchar(20) DEFAULT NULL,
  `Bahan_Bakar` varchar(20) DEFAULT NULL,
  `Harga_Sewa_Per_Hari` decimal(12,2) DEFAULT NULL,
  `Status_Kendaraan` varchar(50) DEFAULT NULL,
  `ID_Cabang` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Kendaraan`),
  UNIQUE KEY `Nomor_Polisi` (`Nomor_Polisi`),
  KEY `ID_Cabang` (`ID_Cabang`),
  CONSTRAINT `kendaraan_ibfk_1` FOREIGN KEY (`ID_Cabang`) REFERENCES `cabang` (`ID_Cabang`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `pegawai`
DROP TABLE IF EXISTS `pegawai`;
CREATE TABLE `pegawai` (
  `NIK_Pegawai` varchar(50) NOT NULL,
  `Nama_Lengkap` varchar(100) DEFAULT NULL,
  `Alamat` text DEFAULT NULL,
  `Nomor_Telepon` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Tanggal_Lahir` date DEFAULT NULL,
  `Jenis_Kelamin` varchar(20) DEFAULT NULL,
  `Jabatan` varchar(50) DEFAULT NULL,
  `ID_Cabang` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`NIK_Pegawai`),
  KEY `ID_Cabang` (`ID_Cabang`),
  CONSTRAINT `pegawai_ibfk_1` FOREIGN KEY (`ID_Cabang`) REFERENCES `cabang` (`ID_Cabang`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `gps_log`
DROP TABLE IF EXISTS `gps_log`;
CREATE TABLE `gps_log` (
  `ID_Log` varchar(50) NOT NULL,
  `Longitude` float DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ID_Kendaraan` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Log`),
  KEY `ID_Kendaraan` (`ID_Kendaraan`),
  CONSTRAINT `gps_log_ibfk_1` FOREIGN KEY (`ID_Kendaraan`) REFERENCES `kendaraan` (`ID_Kendaraan`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `member`
DROP TABLE IF EXISTS `member`;
CREATE TABLE `member` (
  `ID_Member` varchar(50) NOT NULL,
  `Tipe_Member` varchar(50) DEFAULT NULL,
  `Tanggal_Bergabung` date DEFAULT NULL,
  `Status_Member` varchar(50) DEFAULT NULL,
  `Harga_Langganan` decimal(12,2) DEFAULT NULL,
  `Tanggal_Mulai_Langganan` date DEFAULT NULL,
  `Tanggal_Berakhir_Langganan` date DEFAULT NULL,
  `Status_Langganan` varchar(50) DEFAULT NULL,
  `Persentase_Diskon` int DEFAULT NULL,
  `ID_Pelanggan` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Member`),
  KEY `ID_Pelanggan` (`ID_Pelanggan`),
  CONSTRAINT `member_ibfk_1` FOREIGN KEY (`ID_Pelanggan`) REFERENCES `pelanggan` (`ID_Pelanggan`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `penyewaan`
DROP TABLE IF EXISTS `penyewaan`;
CREATE TABLE `penyewaan` (
  `ID_Sewa` varchar(50) NOT NULL,
  `Tanggal_Pesan` datetime DEFAULT NULL,
  `Tanggal_Mulai_Sewa` datetime DEFAULT NULL,
  `Tanggal_Akhir_Sewa` datetime DEFAULT NULL,
  `Tanggal_Pengembalian` datetime DEFAULT NULL,
  `Total_Biaya` decimal(12,2) DEFAULT NULL,
  `Status_Pengembalian` varchar(50) DEFAULT NULL,
  `ID_Pelanggan` varchar(50) DEFAULT NULL,
  `ID_Kendaraan` varchar(50) DEFAULT NULL,
  `NIK_Pegawai` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Sewa`),
  KEY `ID_Pelanggan` (`ID_Pelanggan`),
  KEY `ID_Kendaraan` (`ID_Kendaraan`),
  KEY `NIK_Pegawai` (`NIK_Pegawai`),
  CONSTRAINT `penyewaan_ibfk_1` FOREIGN KEY (`ID_Pelanggan`) REFERENCES `pelanggan` (`ID_Pelanggan`) ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT `penyewaan_ibfk_2` FOREIGN KEY (`ID_Kendaraan`) REFERENCES `kendaraan` (`ID_Kendaraan`) ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT `penyewaan_ibfk_3` FOREIGN KEY (`NIK_Pegawai`) REFERENCES `pegawai` (`NIK_Pegawai`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Struktur tabel `pembayaran`
DROP TABLE IF EXISTS `pembayaran`;
CREATE TABLE `pembayaran` (
  `ID_Bayar` varchar(50) NOT NULL,
  `Tanggal_Bayar` datetime DEFAULT NULL,
  `Metode_Bayar` varchar(50) DEFAULT NULL,
  `Status_Bayar` varchar(50) DEFAULT NULL,
  `ID_Sewa` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Bayar`),
  KEY `ID_Sewa` (`ID_Sewa`),
  CONSTRAINT `pembayaran_ibfk_1` FOREIGN KEY (`ID_Sewa`) REFERENCES `penyewaan` (`ID_Sewa`) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS=1;
