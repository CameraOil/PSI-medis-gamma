Folder ini berisikan core.py dan config.json

Data dari sensor akan tersimpan pada config.json dan diakses melalui core.py

Pada core.py terdapat fungsi-fungsi yang dapat digunakan untuk mengirim data berupa json ke server

Ada dua skenario penggunaan core.py, yaitu dijalankan sebagai main atau di-import
1. Jika dijalankan sebagai main, file config.json harus ada dalam folder
dan masukan sensor harus disimpan pada config.json, sehingga data sensor dapat dikirim ke server.

2. Jika di-import, yawis import aja dan digunakan pada file yang sama saat mengukur sensor (rekomendasi). Metode ini lebih 
fleksibel dan tidak memerlukan inisiasi yang rumit

PENTING: Dibutuhkan file .env yang tersimpan pada folder yang sama. Isi dari file ini harus diisi dengan BASE_URL, EMAIL, dan PASSWORD dari node.
BASE_URL merupakan url home dari server 192.168.xxx.xx, sedangkan EMAIL dan PASSWORD adalah akun yang digunakan node. Jika node belum memiliki
EMAIL dan PASSWORD. Buatlah terlebih dahulu pada laman admin dan tambah baris node pada tabel Nodess dengan akun user node yang baru dibuat
