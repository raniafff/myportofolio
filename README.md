Nama : Rania Firsa

NPM : 2506616693

Kelas : PBP C

Hobi : Membaca buku


### Tugas 1

1. **Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**
   * Ya, saya menggunakan elemen semantik HTML5 seperti `<section>` dan `<article>`. Penggunaan elemen ini sangat membantu dalam menyusun struktur tata letak *static web* agar lebih bermakna dan terorganisir dengan jelas (misalnya memisahkan bagian *hero*, *about*, *projects*, dan detail item portofolio). Selain itu, elemen semantik mempermudah pembacaan kode, meningkatkan aksesibilitas bagi pembaca layar, serta membantu *search engine optimization* (SEO).

2. **Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**
   * Tantangan utamanya adalah menjaga agar tata letak elemen yang semula berdampingan secara horizontal di layar *desktop* (menggunakan *Flexbox* atau *Grid*) tidak berantakan atau terpotong saat dibuka di layar *mobile* yang sempit. Evaluasinya dilakukan dengan melihat hierarki visual informasi; elemen utama seperti judul dan deskripsi diprioritaskan untuk tampil penuh secara vertikal (*stacking*), sementara elemen pelengkap atau gambar diatur ulang ukuran *padding* dan *font*-nya menggunakan *media queries* agar tetap nyaman dibaca di layar kecil.

3. **Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**
   * Batasan utamanya adalah data yang ditampilkan bersifat statis dan kaku (hardcoded di dalam HTML). Setiap kali ingin menambah, mengubah, atau menghapus proyek maupun riwayat pendidikan, kita harus mengubah kodenya secara manual di file kode sumber lalu mengunggahnya kembali. Fungsionalitas dinamis yang paling ingin dipersiapkan dan ditambahkan adalah sistem manajemen data berbasis basis data dengan fitur formulir interaktif (CRUD: *Create, Read, Update, Delete*) serta pengiriman data asinkron/JSON agar portofolio menjadi lebih dinamis dan fleksibel.


### Tugas 2

1. **Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.**
   * **`urls.py` Proyek**: Berfungsi sebagai pintu gerbang utama yang menerima *request* dari peramban pengguna, lalu mencocokkan pola URL tersebut dan meneruskannya (*routing*) ke `urls.py` yang ada di dalam aplikasi spesifik.
   * **`urls.py` Aplikasi**: Menerima arahan dari *urls* proyek untuk mencocokkan pola URL yang lebih spesifik dan memanggil fungsi *view* yang sesuai.
   * **`view`**: Berfungsi sebagai otak logika. Fungsi *view* akan dipanggil ketika URL cocok, lalu mengambil data dari basis data menggunakan *model*, memprosesnya, dan menyiapkan data tersebut ke dalam bentuk konteks.
   * **`model`**: Berfungsi sebagai representasi struktur data di basis data (database). *Model* berinteraksi langsung dengan database untuk mengambil data portofolio yang diminta oleh *view*.
   * **`template`**: Berfungsi untuk merender tampilan antarmuka (HTML). *View* mengirimkan data yang sudah diambil ke *template*, lalu *template* mengubahnya menjadi halaman web utuh yang siap dikirim kembali ke *browser* pengguna.

2. **Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**
   * Menyimpan data pada *model* (database) membuat data bersifat dinamis dan terpusat, sehingga kita bisa melakukan penambahan, perubahan, atau penghapusan data dengan mudah melalui form atau panel admin tanpa harus mengubah kode sumber HTML secara manual setiap ada pembaruan. 
   * **Dampaknya**: Dari sisi pemeliharaan (*maintainability*), aplikasi menjadi jauh lebih bersih dan terstruktur karena pemisahan tugas (*separation of concerns*) antara logika data dan tampilan terjaga dengan baik. Dari sisi pengembangan, akan lebih mudah jika ke depannya ingin dikembangkan fitur interaktif seperti CRUD, *filtering*, atau pengiriman data berbasis JSON.

3. **Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**
   * **`makemigrations`**: Berfungsi untuk mendeteksi adanya perubahan pada file `models.py` (seperti membuat model baru, menambah/menghapus *field*) dan menerjemahkannya menjadi sebuah berkas *blueprint* atau skrip migrasi baru di folder `migrations`. Perintah ini belum menyentuh atau mengubah struktur fisik basis data secara langsung.
   * **`migrate`**: Berfungsi untuk mengeksekusi berkas skrip migrasi tersebut agar perubahan struktur model benar-benar diterapkan dan dibuatkan tabelnya di dalam basis data yang sebenarnya.
   * **Contoh Perubahan**: Ketika kita menambahkan model baru seperti kelas `Education` atau menambah *field* baru (misalnya `is_current = models.BooleanField()`) pada model yang sudah ada, kita wajib menjalankan `makemigrations` terlebih dahulu untuk membuat file cetak biru migrasinya, lalu menjalankan `migrate` untuk menerapkannya ke database.


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