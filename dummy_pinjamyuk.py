
from faker import Faker
import random
from datetime import datetime, timedelta

JUMLAH_CABANG = 10
JUMLAH_PELANGGAN = 2000
JUMLAH_KENDARAAN = 500
JUMLAH_PEGAWAI = 100
JUMLAH_MEMBER = 800
JUMLAH_PENYEWAAN = 10000
JUMLAH_PEMBAYARAN = 10000
JUMLAH_GPS = 3000

CABANG_REAL = [
    {"id": "CB001", "nama": "Cabang Bandung Buah Batu", "kota": "Bandung", "prov": "Jawa Barat", "plat": "D", "jalan": "Jl. Buah Batu No. 123"},
    {"id": "CB002", "nama": "Cabang Jakarta Selatan", "kota": "Jakarta", "prov": "DKI Jakarta", "plat": "B", "jalan": "Jl. TB Simatupang No. 45"},
    {"id": "CB003", "nama": "Cabang Surabaya Gubeng", "kota": "Surabaya", "prov": "Jawa Timur", "plat": "L", "jalan": "Jl. Raya Gubeng No. 88"},
    {"id": "CB004", "nama": "Cabang Bogor Pajajaran", "kota": "Bogor", "prov": "Jawa Barat", "plat": "F", "jalan": "Jl. Pajajaran No. 20"},
    {"id": "CB005", "nama": "Cabang Tangerang BSD", "kota": "Tangerang", "prov": "Banten", "plat": "B", "jalan": "Jl. BSD Raya No. 10"},
    {"id": "CB006", "nama": "Cabang Semarang Tembalang", "kota": "Semarang", "prov": "Jawa Tengah", "plat": "H", "jalan": "Jl. Prof Soedarto No. 5"},
    {"id": "CB007", "nama": "Cabang Yogyakarta Malioboro", "kota": "Yogyakarta", "prov": "DI Yogyakarta", "plat": "AB", "jalan": "Jl. Malioboro No. 99"},
    {"id": "CB008", "nama": "Cabang Bekasi Jatiasih", "kota": "Bekasi", "prov": "Jawa Barat", "plat": "B", "jalan": "Jl. Jatiasih No. 77"},
    {"id": "CB009", "nama": "Cabang Medan Polonia", "kota": "Medan", "prov": "Sumatera Utara", "plat": "BK", "jalan": "Jl. Polonia No. 33"},
    {"id": "CB010", "nama": "Cabang Bali Denpasar", "kota": "Denpasar", "prov": "Bali", "plat": "DK", "jalan": "Jl. Sunset Road No. 12"},
]

KOTA_LIST = [
    ("Bandung", "Jawa Barat"), ("Jakarta", "DKI Jakarta"), ("Surabaya", "Jawa Timur"),
    ("Bogor", "Jawa Barat"), ("Tangerang", "Banten"), ("Semarang", "Jawa Tengah"),
    ("Yogyakarta", "DI Yogyakarta"), ("Bekasi", "Jawa Barat"), ("Medan", "Sumatera Utara"), ("Denpasar", "Bali")
]

fake = Faker('id_ID')
Faker.seed(28)
random.seed(28)

def rand_date(sy=2022, ey=2025):
    s = datetime(sy,1,1); e = datetime(ey,12,31)
    return s + timedelta(days=random.randint(0,(e-s).days))

def clean(t):
    return str(t).replace("'", "").replace("\n", " ")

merek_model = [("Toyota","Avanza"),("Toyota","Innova"),("Daihatsu","Xenia"),("Honda","Brio"),("Honda","HR-V"),("Suzuki","Ertiga"),("Mitsubishi","Xpander")]
warna_list = ["Hitam","Putih","Silver","Merah","Abu-abu"]
jabatan_list = ["Admin","Staff","Manager","Driver","CS"]
tipe_member_list = ["Silver","Gold","Platinum"]

cabang_ids = [c["id"] for c in CABANG_REAL]
pelanggan_ids = [f"PLG{i:05d}" for i in range(1, JUMLAH_PELANGGAN+1)]
kendaraan_ids = [f"KEND{i:05d}" for i in range(1, JUMLAH_KENDARAAN+1)]
pegawai_ids = [f"PEG{i:04d}" for i in range(1, JUMLAH_PEGAWAI+1)]

# PLAT UNIK SESUAI DAERAH CABANG
letters = [f"{chr(65+i)}{chr(65+j)}" for i in range(26) for j in range(26)]
plat_data = []  # list of (plat, cabang_id)
used = set()
idx = 0
for c in CABANG_REAL:
    for _ in range(50):  # 50 mobil per cabang = 500 total
        plat = f"{c['plat']} {1000+idx} {letters[idx % len(letters)]}"
        idx += 1
        if plat not in used:
            used.add(plat)
            plat_data.append((plat, c['id']))
random.shuffle(plat_data)

print("Generating SQL REALISTIS...")

with open("rentalpinjam_dummy_REALISTIS.sql", "w", encoding="utf-8") as f:
    f.write("USE rentalpinjam;\nSET FOREIGN_KEY_CHECKS=0;\nSET AUTOCOMMIT=0;\n")
    f.write("TRUNCATE TABLE pembayaran; TRUNCATE TABLE gps_log; TRUNCATE TABLE penyewaan; TRUNCATE TABLE member; TRUNCATE TABLE kendaraan; TRUNCATE TABLE pegawai; TRUNCATE TABLE pelanggan; TRUNCATE TABLE cabang;\n")

    # CABANG REALISTIS
    print("1. Cabang")
    vals = []
    for c in CABANG_REAL:
        alamat = f"{c['jalan']}, {c['kota']}, {c['prov']}"
        vals.append(f"('{c['id']}','{clean(c['nama'])}','{clean(alamat)}','08{random.randint(1000000000,9999999999)}',{random.randint(5,30)},{random.randint(20,80)})")
    f.write("\n-- CABANG REALISTIS\nINSERT INTO cabang VALUES\n" + ",\n".join(vals) + ";\n")

    # PELANGGAN - kota dan alamat sinkron
    print("2. Pelanggan")
    for bs in range(0, JUMLAH_PELANGGAN, 500):
        batch = pelanggan_ids[bs:bs+500]
        vals = []
        for pid in batch:
            kota, prov = random.choice(KOTA_LIST)
            jalan = f"Jl. {fake.street_name()} No. {random.randint(1,200)}"
            alamat = f"{jalan}, {kota}, {prov}"
            nik = f"32{random.randint(1000000000000000,9999999999999999)}"[:20]
            if hasattr(fake, 'nik'):
                try: nik = fake.nik()
                except: pass
            vals.append(f"('{pid}','{nik}','{clean(fake.name())}','{clean(alamat)}','{fake.phone_number()[:20]}','{fake.email()}','{fake.date_of_birth(minimum_age=17, maximum_age=60)}','{random.choice(['Laki-laki','Perempuan'])}','{random.choice(['Member','Non-Member'])}','Aktif')")
        f.write("\nINSERT INTO pelanggan VALUES\n" + ",\n".join(vals) + ";\n")

    # KENDARAAN - plat sesuai daerah cabang
    print("3. Kendaraan - plat sesuai cabang")
    for bs in range(0, JUMLAH_KENDARAAN, 100):
        batch_kids = kendaraan_ids[bs:bs+100]
        batch_plat = plat_data[bs:bs+100]
        vals = []
        for kid, (nopol, id_cabang) in zip(batch_kids, batch_plat):
            merek, model = random.choice(merek_model)
            vals.append(f"('{kid}','{nopol}','{merek}','{model}',{random.randint(2019,2025)},'{random.choice(warna_list)}',{random.choice([5,7])},'MPV','{random.choice(['Manual','Automatic'])}','Bensin',{random.randint(300000,1500000)},'Tersedia','{id_cabang}')")
        f.write("\nINSERT IGNORE INTO kendaraan VALUES\n" + ",\n".join(vals) + ";\n")

    # PEGAWAI - alamat sesuai cabang tempat kerja
    print("4. Pegawai")
    vals = []
    for pid in pegawai_ids:
        c = random.choice(CABANG_REAL)
        alamat = f"Jl. {fake.street_name()} No. {random.randint(1,100)}, {c['kota']}, {c['prov']}"
        vals.append(f"('{pid}','{clean(fake.name())}','{clean(alamat)}','{fake.phone_number()[:20]}','{fake.email()}','{fake.date_of_birth(minimum_age=20, maximum_age=50)}','{random.choice(['Laki-laki','Perempuan'])}','{random.choice(jabatan_list)}','{c['id']}')")
    f.write("\nINSERT INTO pegawai VALUES\n" + ",\n".join(vals) + ";\n")

    # MEMBER
    print("5. Member")
    member_ids = [f"MEM{i:05d}" for i in range(1, JUMLAH_MEMBER+1)]
    sample_pel = random.sample(pelanggan_ids, JUMLAH_MEMBER)
    for bs in range(0, JUMLAH_MEMBER, 500):
        bm = member_ids[bs:bs+500]; bp = sample_pel[bs:bs+500]
        vals = []
        for mid, pel_id in zip(bm, bp):
            tipe = random.choice(tipe_member_list)
            tgl_gabung = rand_date(2022, 2024).date()
            tgl_akhir = (datetime.combine(tgl_gabung, datetime.min.time()) + timedelta(days=365)).date()
            harga = {"Silver":100000,"Gold":200000,"Platinum":500000}[tipe]
            diskon = {"Silver":5,"Gold":10,"Platinum":20}[tipe]
            vals.append(f"('{mid}','{tipe}','{tgl_gabung}','Aktif',{harga},'{tgl_gabung}','{tgl_akhir}','Aktif',{diskon},'{pel_id}')")
        f.write("\nINSERT INTO member VALUES\n" + ",\n".join(vals) + ";\n")

    # PENYEWAAN
    print("6. Penyewaan 10k")
    sewa_ids = [f"SEWA{i:06d}" for i in range(1, JUMLAH_PENYEWAAN+1)]
    for bs in range(0, JUMLAH_PENYEWAAN, 500):
        batch = sewa_ids[bs:bs+500]
        vals = []
        for sid in batch:
            tgl_pesan = rand_date(2024, 2025)
            tgl_mulai = tgl_pesan + timedelta(days=random.randint(0,2))
            lama = random.randint(1,7)
            tgl_akhir = tgl_mulai + timedelta(days=lama)
            kembali = tgl_akhir + timedelta(days=random.randint(0,1)) if random.random() > 0.2 else None
            kembali_str = f"'{kembali}'" if kembali else "NULL"
            total = lama * random.randint(200000, 1000000)
            vals.append(f"('{sid}','{tgl_pesan}','{tgl_mulai}','{tgl_akhir}',{kembali_str},{total},'{random.choice(['Sudah Kembali','Belum Kembali','Terlambat'])}','{random.choice(pelanggan_ids)}','{random.choice(kendaraan_ids)}','{random.choice(pegawai_ids)}')")
        f.write("\nINSERT INTO penyewaan VALUES\n" + ",\n".join(vals) + ";\n")

    # PEMBAYARAN
    print("7. Pembayaran")
    bayar_ids = [f"BAYAR{i:06d}" for i in range(1, JUMLAH_PEMBAYARAN+1)]
    for bs in range(0, JUMLAH_PEMBAYARAN, 500):
        batch = bayar_ids[bs:bs+500]
        vals = []
        for i, bid in enumerate(batch):
            sewa_id = sewa_ids[bs + i]
            vals.append(f"('{bid}','{rand_date(2024,2025)}','{random.choice(['Transfer','Cash','E-Wallet'])}','{random.choice(['Lunas','Pending'])}','{sewa_id}')")
        f.write("\nINSERT INTO pembayaran VALUES\n" + ",\n".join(vals) + ";\n")

    # GPS
    print("8. GPS")
    log_ids = [f"LOG{i:06d}" for i in range(1, JUMLAH_GPS+1)]
    for bs in range(0, JUMLAH_GPS, 500):
        batch = log_ids[bs:bs+500]
        vals = []
        for lid in batch:
            vals.append(f"('{lid}',{random.uniform(106.7,107.7):.6f},{random.uniform(-6.9,-6.1):.6f},NOW(),'{random.choice(kendaraan_ids)}')")
        f.write("\nINSERT INTO gps_log VALUES\n" + ",\n".join(vals) + ";\n")

    f.write("\nSET FOREIGN_KEY_CHECKS=1;\nCOMMIT;\n")

print("Done bosku - REALISTIS!")
