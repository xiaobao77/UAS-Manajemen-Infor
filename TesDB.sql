CREATE TABLE produk (
    id_produk INT PRIMARY KEY,
    nama_produk VARCHAR(100),
    jenis_produk VARCHAR(100),
    harga DECIMAL(10, 2),
    stok INT
);

CREATE TABLE pembelian (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pembeli VARCHAR(100),
    nama_produk VARCHAR(100),
    jumlah INT,
    total_harga DECIMAL(10, 2),
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Menambahkan data contoh ke tabel Produk
INSERT INTO Produk (id_produk, nama_produk, jenis_produk, harga, stok) VALUES 
(1, 'Teh Dingin', 'Minuman', 10000.00, 50),
(2, 'Americano', 'Minuman', 20000.00, 30),
(3, 'Mie Goreng', 15000.00, 20);
