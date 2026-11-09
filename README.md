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


### Tugas 5

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**
   * **Pengertian Debouncing**: *Debouncing* adalah teknik pemrograman yang digunakan untuk membatasi frekuensi pemanggilan suatu fungsi dengan cara menunda eksekusi fungsi tersebut sampai sejumlah waktu jeda tertentu telah berlalu sejak *event* terakhir dipicu. Jika *event* yang sama kembali dipicu sebelum waktu jeda (*delay*) berakhir, maka *timer* sebelumnya akan dibatalkan (`clearTimeout`) dan dihitung ulang dari awal.
   * **Pentingnya pada fitur pencarian AJAX**:
     * **Mengurangi Beban Server (*Prevent Request Overload*)**: Tanpa *debouncing*, setiap kali pengguna mengetikkan satu karakter (*event* `input`), aplikasi akan langsung mengirim *HTTP request* ke server. Jika pengguna mengetik kata pencarian sepanjang 10 karakter dengan cepat, akan terjadi 10 permintaan ke server berturut-turut dalam hitungan detik. Dengan *debouncing* (misalnya jeda 300 ms), *request* hanya akan dikirim 1 kali setelah pengguna selesai mengetik.
     * **Menghemat Penggunaan *Bandwidth* Jaringan**: Mengurangi lalu lintas data *request* dan *response* JSON yang sebenarnya tidak diperlukan antara klien dan server.
     * **Mencegah Masalah *Race Condition***: Jika setiap ketukan mengirim *request*, respons dari *request* sebelumnya yang lambat bisa saja baru tiba setelah respons dari *request* terbaru. Hal ini dapat menyebabkan data yang tampil di layar tidak sinkron dengan kata kunci terakhir yang diinginkan oleh pengguna.

2. **Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?**
   * **Fungsi `await` pada `fetch()`**: `fetch()` adalah operasi asinkron yang mengembalikan sebuah objek `Promise`. Kata kunci `await` berfungsi untuk menangguhkan (*pause*) kelanjutan eksekusi baris kode di dalam fungsi `async` sampai `Promise` tersebut selesai diproses (*resolved* atau *rejected*), lalu langsung mengekstrak nilai hasilnya (yaitu objek `Response`). Hal ini memungkinkan kita menulis kode penanganan asinkron dengan gaya sekuensial yang bersih, terstruktur, dan mudah dibaca layaknya kode sinkron.
   * **Apa yang terjadi jika tidak menggunakan `await`**:
     * Jika kita memanggil `const response = fetch(url);` tanpa `await`, variabel `response` tidak akan berisi objek data `Response`, melainkan objek `Promise <pending>`.
     * Saat kita mencoba mengakses properti atau *method* bawaan respons (seperti `response.ok` atau `response.json()`), operasi tersebut akan gagal atau menghasilkan *Promise* lain yang belum terselesaikan karena data respons dari jaringan belum selesai diterima.
     * Akibatnya, alur program akan langsung berlanjut ke baris berikutnya sebelum data berhasil diambil, sehingga data tidak dapat langsung dirender ke layar kecuali jika ditangani secara manual menggunakan rantai callback `.then()` dan `.catch()`.

3. **Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**
   * **Pengertian Serangan XSS (*Cross-Site Scripting*)**: XSS adalah kerentanan keamanan web di mana penyerang berhasil menyuntikkan skrip berbahaya (biasanya berupa kode JavaScript jahat) ke dalam sebuah aplikasi web yang kemudian dieksekusi di peramban pengguna lain. Serangan ini dapat dimanfaatkan untuk mencuri data sensitif (seperti *session cookies*, token JWT, atau kredensial autentikasi), melakukan pembajakan sesi (*session hijacking*), manipulasi tampilan halaman web, maupun mengarahkan pengguna ke situs palsu (*phishing*).
   * **Mengapa data via AJAX/JavaScript lebih rentan dibandingkan template Django**:
     * **Perlindungan Otomatis (*Auto-escaping*) pada Django Template**: Secara *default*, sistem *template engine* Django secara otomatis melakukan *HTML auto-escaping* terhadap semua variabel konteks yang disisipkan ke halaman HTML. Karakter-karakter berisiko seperti `<`, `>`, `&`, `"`, dan `'` otomatis diubah menjadi entitas HTML aman (`&lt;`, `&gt;`, dsb.), sehingga skrip jahat tidak akan dieksekusi sebagai tag HTML.
     * **Ketiadaan *Auto-escaping* saat Manipulasi DOM dengan JavaScript**: Ketika data diambil melalui AJAX dalam format JSON, peramban menerimanya sebagai data mentah. Jika data tersebut disisipkan ke dokumen web menggunakan manipulasi *DOM* seperti `innerHTML` atau *template literals* (misalnya `element.innerHTML = '<div>' + data.text + '</div>'`), peramban akan langsung mem-parsing dan mengeksekusi string tersebut sebagai HTML dan JavaScript murni. Jika input tersebut mengandung tag seperti `<script>` atau `<img src="x" onerror="alert('XSS')">`, skrip tersebut akan langsung dieksekusi tanpa filter. Oleh karena itu, saat menggunakan AJAX/JavaScript, pengembang wajib menerapkan sanitasi ganda: membersihkan input berbahaya di sisi server (menggunakan `strip_tags` di formulir Django) dan melakukan *manual escaping* (misalnya dengan fungsi `escapeHtml()` atau menggunakan properti aman seperti `.textContent`) di sisi klien sebelum data ditampilkan ke DOM.



### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful!**
   * **Pengertian REST (*Representational State Transfer*)**: REST adalah gaya arsitektur perangkat lunak untuk sistem terdistribusi dan komunikasi antar-layanan berbasis web (*web services*) yang diperkenalkan oleh Roy Fielding pada tahun 2000. REST mendefinisikan seperangkat prinsip atau batasan (*constraints*), antara lain: arsitektur *Client-Server*, sifat *Stateless* (setiap permintaan dari klien harus memuat seluruh informasi yang diperlukan tanpa bergantung pada sesi di server), *Cacheable*, *Layered System*, serta antarmuka seragam (*Uniform Interface*) yang mengatur manipulasi sumber daya (*resources*) melalui representasi data, pesan yang deskriptif (*self-descriptive messages*), dan *HATEOAS* (*Hypermedia as the Engine of Application State*).
   * **Mengapa mengembalikan JSON saja belum cukup disebut RESTful**:
     * JSON hanyalah format serialisasi muatan data (*data interchange format / representation payload*).
     * Sebuah API dapat saja mengembalikan data dalam format JSON tetapi melanggar prinsip-prinsip inti REST. Contohnya, API yang menggunakan pola RPC (*Remote Procedure Call*) di mana seluruh aksi hanya menggunakan satu metode HTTP `POST` dengan endpoint kata kerja (seperti `/api/create_project/` atau `/api/delete_project/`), mengabaikan kode status HTTP standar (misal selalu mengembalikan `200 OK` meskipun terjadi *error* di server), atau menyimpan status percakapan pengguna di memori server (*stateful*).
     * Untuk dapat disebut sebagai **RESTful**, API wajib mematuhi arsitektur REST secara holistik: memanfaatkan URI sebagai identifikasi kata benda (*nouns*) untuk setiap *resource* (misalnya `/api/v1/projects/`), memanfaatkan metode HTTP (*verbs*) sesuai semantik standarnya (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), mengembalikan kode status HTTP yang semantik (`200`, `201`, `204`, `400`, `403`, `404`), serta bersifat *stateless*.

2. **Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**
   * **Perbedaan PUT dan PATCH**:
     * **`PUT` (Full Replacement / Overwrite)**: Digunakan untuk mengganti keseluruhan representasi suatu *resource* yang sudah ada dengan representasi baru yang dikirimkan oleh klien. Klien diwajibkan mengirimkan seluruh atribut objek secara lengkap. Jika ada atribut opsional yang tidak disertakan dalam *payload*, server umumnya akan mengatur atribut tersebut kembali ke nilai bawaan (*default*) atau `null`. Operasi `PUT` bersifat idempoten (*idempotent*), artinya pemanggilan `PUT` berkali-kali dengan *payload* yang sama akan menghasilkan status akhir data yang sama di server.
     * **`PATCH` (Partial Update)**: Digunakan untuk memperbarui sebagian (*partial*) atribut dari suatu *resource* tanpa mengubah atribut lainnya. Klien hanya perlu mengirimkan kunci-nilai dari atribut yang ingin diubah. Operasi `PATCH` tidak diwajibkan bersifat idempoten menurut spesifikasi HTTP (walaupun dalam praktik pembaruan field sering kali menghasilkan efek yang idempoten).
   * **Contoh Penggunaan**:
     * **Contoh `PUT`**: Ketika pengguna membuka formulir edit proyek portofolio secara menyeluruh dan menekan tombol simpan, di mana klien mengirimkan seluruh data entitas proyek sekaligus:  
       `PUT /api/v1/projects/<id>/`  
       *Payload:* `{"title": "Website Portofolio", "description": "Deskripsi lengkap...", "tech_stack": "Django, DRF", "project_url": "https://example.com", "project_image_url": "https://example.com/img.png"}`.
     * **Contoh `PATCH`**: Ketika kita hanya ingin mengubah satu atribut tertentu, misalnya hanya memperbarui judul proyek atau mengubah tautan proyek tanpa perlu memuat ulang atau mengirim ulang teks deskripsi panjang dan *tech stack*:  
       `PATCH /api/v1/projects/<id>/`  
       *Payload:* `{"title": "Website Portofolio v2"}`.

3. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**
   * **Peran Serializer**:
     * Berfungsi sebagai jembatan konversi dua arah (*two-way converter*):
       1. **Serialisasi (*Serialization*)**: Mengubah objek model Django yang kompleks (seperti instance model ORM atau *QuerySet*) menjadi tipe data Python bawaan (*native* seperti *dictionary*, *list*) yang dapat dirender dengan mudah menjadi format JSON atau XML untuk dikirim ke klien.
       2. **Deserialisasi & Validasi (*Deserialization & Validation*)**: Mengonversi *payload* JSON/data masuk dari klien kembali menjadi data Python yang divalidasi integritasnya, lalu menyimpannya sebagai objek model ke dalam basis data.
   * **Keuntungan Serializer dibandingkan merakit dictionary manual dengan `JsonResponse`**:
     * **Validasi Terstruktur dan Otomatis**: Serializer menyediakan mekanisme validasi data bawaan (`is_valid()`, `errors`) yang setara dengan Django Forms. Serializer memvalidasi tipe data, panjang string, aturan keunikan (*uniqueness*), format URL/email, hingga validasi khusus per-field (`validate_<field>()`) tanpa perlu menulis puluhan baris logika percabangan `if-else` secara manual.
     * **Pencegahan Kerentanan (*Mass Assignment*) & Keamanan Data**: Dengan menentukan daftar `fields` secara eksplisit, kita memastikan bahwa hanya field yang diizinkan saja yang dapat diakses atau diubah oleh klien. Data sensitif (seperti *password hash*) tidak akan terekspos secara tidak sengaja.
     * **Dukungan *Computed Fields* yang Bersih**: Memungkinkan penambahan data kalkulasi dinamis (seperti `SerializerMethodField` untuk menghitung `star_count` dan mengecek `is_starred`) secara rapi dan terpusat.
     * **Prinsip DRY (*Don't Repeat Yourself*)**: Struktur representasi dan validasi data terpusat dalam satu kelas serializer yang dapat digunakan kembali di berbagai endpoint API yang berbeda.

4. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**
   * **Perbedaan Autentikasi dan Otorisasi**:
     * **Autentikasi (*Authentication*)**: Proses untuk membuktikan dan memverifikasi **identitas** pengguna yang melakukan *request* (*"Who are you?"*). DRF memeriksa kredensial (seperti *session cookie*, *token*, atau kredensial pengguna) dan mengaitkan permintaan tersebut dengan objek `request.user` (apakah pengguna adalah *AnonymousUser* atau pengguna yang sah).
     * **Otorisasi (*Authorization*)**: Proses untuk menentukan **izin atau hak akses** yang dimiliki oleh pengguna yang identitasnya telah terverifikasi tersebut (*"What are you allowed to do?"*). DRF memeriksa apakah pengguna tersebut diperbolehkan melakukan aksi tertentu (misalnya membaca, mengedit, menambah, atau menghapus suatu *resource*).
   * **Mengapa hak akses harus diperiksa di server via *permission class***:
     * Menyembunyikan tombol aksi pada *template* HTML hanyalah kontrol tampilan di sisi antarmuka (*client-side UI*). Pengguna mana pun (termasuk pihak yang berniat jahat atau pengguna biasa yang memiliki pemahaman teknis dasar) dapat membuka *Developer Tools* peramban, melihat endpoint URL API, atau langsung mengirimkan permintaan HTTP menggunakan perkakas seperti cURL, Postman, maupun Fetch API dari konsol JavaScript.
     * Jika server tidak dilengkapi pemeriksaan otorisasi (*permission class*), server akan tetap memproses dan mengeksekusi permintaan berbahaya tersebut (seperti menghapus proyek atau memodifikasi data orang lain) meskipun tombol di halaman web tidak ditampilkan. Oleh sebab itu, pemeriksaan hak akses di sisi server adalah benteng pertahanan mutlak (*mandatory security enforcement*) yang tidak dapat dimanipulasi oleh klien.

5. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**
   * **Mengapa tetap memerlukan token CSRF pada `SessionAuthentication`**:
     * `SessionAuthentication` menggunakan mekanisme berbasis cookie peramban (`sessionid`) untuk mengidentifikasi sesi login pengguna.
     * Kelemahan utama autentikasi berbasis cookie adalah serangan *Cross-Site Request Forgery* (CSRF), di mana peramban secara otomatis akan melampirkan cookie sesi milik pengguna setiap kali mengirimkan permintaan ke domain aplikasi target, bahkan jika permintaan tersebut dipicu dari situs web pihak ketiga yang berbahaya (misalnya melalui form tersembunyi atau skrip jahat saat pengguna membuka tab lain).
     * Untuk menangkal serangan ini, Django dan DRF mewajibkan setiap permintaan yang mengubah keadaan (*state-changing methods*: `POST`, `PUT`, `PATCH`, `DELETE`) untuk menyertakan token CSRF yang unik dan sah di dalam header (*X-CSRFToken*) atau form data. Token ini tidak dapat dicuri oleh domain luar karena dilindungi oleh kebijakan *Same-Origin Policy* (SOP) peramban.
   * **Mengapa `force_authenticate` tidak cukup untuk membuktikan perlindungan CSRF**:
     * `force_authenticate` adalah modul utilitas pengujian bawaan DRF (`rest_framework.test`) yang dirancang untuk mempercepat pengujian logika view dan izin akses. Ketika fungsi ini dipanggil, DRF secara langsung menyuntikkan objek pengguna ke `request.user` dan **secara eksplisit melewati (*bypass*) seluruh alur autentikasi dan validasi middleware CSRF Django**.
     * Oleh karena itu, pengujian yang menggunakan `force_authenticate` hanya membuktikan bahwa izin otorisasi (*permission class*) dan logika data pada view bekerja dengan benar untuk pengguna terkait, namun **sama sekali tidak menguji apakah mekanisme penolakan CSRF berfungsi** ketika ada permintaan tanpa token CSRF yang sah. Untuk memverifikasi bahwa perlindungan CSRF benar-benar aktif di lingkungan nyata, pengujian harus dilakukan menggunakan *client* HTTP standar tanpa mem-*bypass* middleware CSRF.


---

### AI Disclosure
* **Tool yang digunakan**: Antigravity Assistant (AI Pair Programmer).
* **Strategi Prompting**: Memberikan instruksi spesifikasi tugas secara bertahap dan terperinci sesuai silabus resmi PBP Fasilkom UI (Gasal 2026/2027), mulai dari instalasi DRF, perancangan Serializer eksplisit dengan pembersihan XSS, implementasi custom permission class empat peran, pembuatan endpoint RESTful `/api/v1/`, integrasi antarmuka asinkron (fetch) tanpa reload halaman, hingga penulisan unit test berbasis `APITestCase`.
* **Bagian yang dibantu**:
  - Penyusunan `ModelSerializer` di `main/serializers.py` dengan computed fields (`star_count`, `is_starred`) dan sanitasi input `strip_tags`.
  - Perancangan aturan otorisasi berbasis peran di `main/permissions.py` (`IsPortfolioOwnerOrEditorOrReadOnly`).
  - Implementasi fungsi API views dengan `@api_view` dan `SessionAuthentication` di `main/api_views.py`.
  - Integrasi antarmuka pada `show_project.html` dan `show_education.html` (modal edit baru, aksi delete, toggle star, dan error handling toast via fetch API).
  - Penulisan skenario pengujian komprehensif pada `main/tests.py` termasuk verifikasi konsistensi isi basis data dan pembuktian penegakan CSRF menggunakan `APIClient(enforce_csrf_checks=True)`.
