Nama : Rania Firsa

NPM : 2506616693

Kelas : PBP C

Hobi : Membaca buku

### Tugas 3

1. **Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!**
   * **Penggunaan `ModelForm`**: `ModelForm` menyederhanakan proses pembuatan form yang terikat langsung dengan model Django. Dengan `ModelForm`, kita tidak perlu mendefinisikan ulang field satu per satu secara manual baik di HTML maupun di file `forms.py`. Django akan secara otomatis menghasilkan elemen form yang sesuai dengan tipe data pada model, serta menyediakan fungsi validasi bawaan (`is_valid()`) dan penyimpanan data (`form.save()`) secara aman dan efisien.
   * **Fungsi `{% csrf_token %}`**: Token ini diwajibkan sebagai mekanisme keamanan untuk mencegah serangan *Cross-Site Request Forgery* (CSRF). Dengan adanya *token* unik pada setiap *request* form, Django dapat memastikan bahwa permintaan *POST* yang dikirim benar-benar berasal dari pengguna yang sah di halaman web tersebut, bukan dari pihak atau situs eksternal yang berniat merusak.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**
   * **Struktur Lebih Ringan dan Ringkas**: JSON (*JavaScript Object Notation*) memiliki sintaks yang jauh lebih sederhana, menggunakan format pasangan kunci-nilai (key-value) dan *array*, sehingga tidak memerlukan tag pembuka dan penutup yang repetitif seperti XML. Hal ini membuat ukuran ukuran file JSON jauh lebih kecil dan menghemat *bandwidth*.
   * **Performa Parsing yang Cepat**: Karena formatnya yang selaras dengan objek JavaScript (dan mudah dipetakan ke struktur data di berbagai bahasa pemrograman lain), proses *parsing* data JSON di sisi klien maupun server berjalan jauh lebih cepat dibandingkan XML yang memerlukan *DOM parser* yang lebih kompleks.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?**
   * **Alur Fungsi View JSON**: 
     1. Klien (pengguna atau sistem luar) mengakses URL yang mengarah ke endpoint JSON.
     2. Fungsi *view* menerima *request* tersebut dan mengambil seluruh data dari basis data menggunakan *QuerySet* (misalnya `Education.objects.all()`).
     3. Data model Django tersebut kemudian diubah (*serialize*) ke dalam format teks JSON menggunakan modul `serializers.serialize()`.
     4. Terakhir, *view* mengembalikan objek `HttpResponse` dengan tipe konten (`content_type`) berupa `application/json`.
   * **Alasan Perlunya *Serialization***: Model Django berbentuk objek Python kompleks yang berinteraksi langsung dengan basis data (ORM) dan tidak bisa dibaca secara langsung oleh protokol HTTP atau aplikasi berbasis web lainnya. Proses *serialization* diperlukan untuk menerjemahkan objek-objek Python tersebut ke dalam format standar yang universal (seperti string JSON) agar dapat dikirim melalui jaringan dan mudah dibaca oleh berbagai jenis platform atau *frontend*.