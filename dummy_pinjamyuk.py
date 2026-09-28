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

fake = Faker('id_ID')
Faker.seed(28)
random.seed(28)

def rand_date(start_year=2022, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end-start).days))

def clean(text):
    """Bersihin kutip biar gak error SQL"""
    return str(text).replace("'", "").replace("\n", " ")

# Data pool agar variatif
merek_model = [("Toyota","Avanza"),("Toyota","Innova"),("Daihatsu","Xenia"),("Honda","Brio"),("Honda","HR-V"),("Suzuki","Ertiga"),("Mitsubishi","Xpander"),("Toyota","Fortuner")]
warna_list = ["Hitam","Putih","Silver","Merah","Abu-abu"]
jabatan_list = ["Admin","Staff","Manager","Driver","CS"]
tipe_member_list = ["Silver","Gold","Platinum"]

# ID
cabang_ids = [f"CB{i:03d}" for i in range(1, JUMLAH_CABANG+1)]
pelanggan_ids = [f"PLG{i:05d}" for i in range(1, JUMLAH_PELANGGAN+1)]
kendaraan_ids = [f"KEND{i:05d}" for i in range(1, JUMLAH_KENDARAAN+1)]
pegawai_ids = [f"PEG{i:04d}" for i in range(1, JUMLAH_PEGAWAI+1)]

print("Generating SQL...")

with open("rentalpinjam_dummy_10k.sql", "w", encoding="utf-8") as f:
    f.write("USE rentalpinjam;\nSET FOREIGN_KEY_CHECKS=0;\nSET AUTOCOMMIT=0;\n")

    # Cabang
    print(f"1. Cabang {JUMLAH_CABANG}")
    vals = []
    for i, cid in enumerate(cabang_ids):
        nama = f"Cabang {fake.city()}"
        alamat = clean(fake.address())
        telp = fake.phone_number()[:20]
        vals.append(f"('{cid}','{clean(nama)}','{alamat}','{telp}',{random.randint(5,30)},{random.randint(20,80)})")
    f.write("\n-- CABANG\nINSERT INTO cabang VALUES\n" + ",\n".join(vals) + ";\n")

    # Pelanggan
    print(f"2. Pelanggan {JUMLAH_PELANGGAN}")
    for batch_start in range(0, JUMLAH_PELANGGAN, 500):
        batch = pelanggan_ids[batch_start:batch_start+500]
        vals = []
        for pid in batch:
            nik = fake.nik() if hasattr(fake, 'nik') else f"32{random.randint(1000000000000000,9999999999999999)}"[:20]
            nama = clean(fake.name())
            alamat = clean(fake.address())
            nohp = fake.phone_number()[:20]
            email = fake.email()
            tgl_lahir = fake.date_of_birth(minimum_age=17, maximum_age=60)
            jk = random.choice(["Laki-laki","Perempuan"])
            vals.append(f"('{pid}','{nik}','{nama}','{alamat}','{nohp}','{email}','{tgl_lahir}','{jk}','{random.choice(['Member','Non-Member'])}','Aktif')")
        f.write("\nINSERT INTO pelanggan VALUES\n" + ",\n".join(vals) + ";\n")

    # Kendaraan
    print(f"3. Kendaraan {JUMLAH_KENDARAAN}")
    for batch_start in range(0, JUMLAH_KENDARAAN, 500):
        batch = kendaraan_ids[batch_start:batch_start+500]
        vals = []
        for kid in batch:
            merek, model = random.choice(merek_model)
            nopol = f"D {random.randint(1000,9999)} {random.choice(['ABC','XYZ','DEF'])}"
            vals.append(f"('{kid}','{nopol}','{merek}','{model}',{random.randint(2018,2025)},'{random.choice(warna_list)}',{random.choice([4,5,7])},'{random.choice(['MPV','SUV'])}','{random.choice(['Manual','Automatic'])}','{random.choice(['Bensin','Solar'])}',{random.randint(200000,1500000)},'{random.choice(['Tersedia','Disewa'])}','{random.choice(cabang_ids)}')")
        f.write("\nINSERT INTO kendaraan VALUES\n" + ",\n".join(vals) + ";\n")

    # Pegawai
    print(f"4. Pegawai {JUMLAH_PEGAWAI}")
    vals = []
    for pid in pegawai_ids:
        nama = clean(fake.name())
        vals.append(f"('{pid}','{nama}','{clean(fake.address())}','{fake.phone_number()[:20]}','{fake.email()}','{fake.date_of_birth(minimum_age=20, maximum_age=50)}','{random.choice(['Laki-laki','Perempuan'])}','{random.choice(jabatan_list)}','{random.choice(cabang_ids)}')")
    f.write("\n-- PEGAWAI\nINSERT INTO pegawai VALUES\n" + ",\n".join(vals) + ";\n")

    # Member
    print(f"5. Member {JUMLAH_MEMBER}")
    member_ids = [f"MEM{i:05d}" for i in range(1, JUMLAH_MEMBER+1)]
    sample_pel = random.sample(pelanggan_ids, JUMLAH_MEMBER)
    for batch_start in range(0, JUMLAH_MEMBER, 500):
        batch_m = member_ids[batch_start:batch_start+500]
        batch_p = sample_pel[batch_start:batch_start+500]
        vals = []
        for mid, pel_id in zip(batch_m, batch_p):
            tipe = random.choice(tipe_member_list)
            tgl_gabung = rand_date(2022, 2024).date()
            tgl_akhir = (datetime.combine(tgl_gabung, datetime.min.time()) + timedelta(days=365)).date()
            harga = {"Silver":100000,"Gold":200000,"Platinum":500000}[tipe]
            diskon = {"Silver":5,"Gold":10,"Platinum":20}[tipe]
            vals.append(f"('{mid}','{tipe}','{tgl_gabung}','Aktif',{harga},'{tgl_gabung}','{tgl_akhir}','Aktif',{diskon},'{pel_id}')")
        f.write("\nINSERT INTO member VALUES\n" + ",\n".join(vals) + ";\n")

    # Penyewaan 
    print(f"6. Penyewaan {JUMLAH_PENYEWAAN}")
    sewa_ids = [f"SEWA{i:06d}" for i in range(1, JUMLAH_PENYEWAAN+1)]
    for batch_start in range(0, JUMLAH_PENYEWAAN, 500):
        batch = sewa_ids[batch_start:batch_start+500]
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

    # Pembayaran
    print(f"7. Pembayaran {JUMLAH_PEMBAYARAN}")
    bayar_ids = [f"BAYAR{i:06d}" for i in range(1, JUMLAH_PEMBAYARAN+1)]
    for batch_start in range(0, JUMLAH_PEMBAYARAN, 500):
        batch = bayar_ids[batch_start:batch_start+500]
        vals = []
        for i, bid in enumerate(batch):
            sewa_id = sewa_ids[batch_start + i]
            vals.append(f"('{bid}','{rand_date(2024,2025)}','{random.choice(['Transfer','Cash','E-Wallet'])}','{random.choice(['Lunas','Pending'])}','{sewa_id}')")
        f.write("\nINSERT INTO pembayaran VALUES\n" + ",\n".join(vals) + ";\n")

    # GPS Log
    print(f"8. GPS Log {JUMLAH_GPS}")
    log_ids = [f"LOG{i:06d}" for i in range(1, JUMLAH_GPS+1)]
    for batch_start in range(0, JUMLAH_GPS, 500):
        batch = log_ids[batch_start:batch_start+500]
        vals = []
        for lid in batch:
            vals.append(f"('{lid}',{random.uniform(106.7,107.7):.6f},{random.uniform(-6.9,-6.1):.6f},NOW(),'{random.choice(kendaraan_ids)}')")
        f.write("\nINSERT INTO gps_log VALUES\n" + ",\n".join(vals) + ";\n")

    f.write("\nSET FOREIGN_KEY_CHECKS=1;\nCOMMIT;\n")

print("Done bosku")
