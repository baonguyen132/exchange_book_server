CREATE DATABASE IF NOT EXISTS `exchange_book` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `exchange_book`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `exchange_book`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `date_purchase` varchar(20) NOT NULL,
  `price` int(11) NOT NULL,
  `description` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `image` varchar(200) NOT NULL,
  `id_user` bigint(20) UNSIGNED NOT NULL,
  `id_type_book` int(20) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `book`
--

INSERT INTO `book` (`id`, `date_purchase`, `price`, `description`, `status`, `quantity`, `image`, `id_user`, `id_type_book`, `created_at`, `updated_at`) VALUES
(39, '2021-12-12', 5000, 'sách còn mới', 1, 1, 'public/image_book_client/book_upload_20251026_055658_a10e2d.jpg', 15, 93, '2025-10-26 05:57:40', '2025-10-26 05:57:40'),
(40, '2021-12-20', 3000, 'sách còn mới', 1, 1, 'public/image_book_client/book_upload_20251026_055831_e73ef3.jpg', 15, 89, '2025-10-26 05:58:54', '2025-10-26 05:58:54');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `status` varchar(100) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `total` int(11) NOT NULL,
  `id_user` bigint(11) UNSIGNED NOT NULL,
  `id_seller` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `cart`
--

INSERT INTO `cart` (`id`, `status`, `address`, `total`, `id_user`, `id_seller`, `created_at`, `updated_at`) VALUES
(54, 'Đã nhận', 'tủ sách đo', 5000, 21, 15, '2025-10-25 23:01:25', '2025-10-25 23:03:20');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `detail_cart`
--

CREATE TABLE `detail_cart` (
  `id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `id_book` int(11) NOT NULL,
  `id_cart` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `detail_cart`
--

INSERT INTO `detail_cart` (`id`, `quantity`, `id_book`, `id_cart`) VALUES
(76, 1, 39, 54);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `images`
--

CREATE TABLE `images` (
  `id` int(11) NOT NULL,
  `path` mediumtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `id_user` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `images`
--

INSERT INTO `images` (`id`, `path`, `status`, `id_user`) VALUES
(4, 'uploads\\048204007137\\IMG_20250308_114323.jpg', '0', 15),
(25, 'uploads/048066007160/f340d3d6-ea02-4ede-bb0d-82f9b4ac047c.jpg', '0', 17);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `transaction`
--

CREATE TABLE `transaction` (
  `id` int(11) NOT NULL,
  `transaction_date` date NOT NULL,
  `price` int(11) NOT NULL,
  `state` tinyint(1) NOT NULL,
  `id_user` bigint(11) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `transaction`
--

INSERT INTO `transaction` (`id`, `transaction_date`, `price`, `state`, `id_user`, `created_at`, `updated_at`) VALUES
(23, '2025-10-08', 50000, 1, 15, '2025-10-08 06:04:05', '2025-10-08 06:04:05'),
(24, '2025-10-08', 50000, 1, 15, '2025-10-08 06:08:22', '2025-10-08 06:08:22'),
(25, '2025-10-08', 50000, 1, 15, '2025-10-08 06:11:53', '2025-10-08 06:11:53');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `type_books`
--

CREATE TABLE `type_books` (
  `id` int(11) NOT NULL,
  `name_book` varchar(100) NOT NULL,
  `type_book` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `type_books`
--

INSERT INTO `type_books` (`id`, `name_book`, `type_book`, `price`, `image`, `description`, `created_at`, `updated_at`) VALUES
(87, 'Âm nhạc 10 - Kết nối tri thức với cuộc sống', 'Sách lớp 10', 10000, 'public/image/book_20251026_054257_7f9f26.jpg', 'Sách Âm nhạc lớp 10 thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức và kỹ năng về âm nhạ', '2025-10-26 05:43:14', '2025-10-26 05:43:14'),
(88, 'Vật lí 11 - Kết nối tri thức với cuộc sống', 'Sách lớp 11', 12000, 'public/image/book_20251026_054346_9fd0f7.png', 'Sách Vật lí lớp 11 thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức cơ bản và nâng cao về', '2025-10-26 05:43:55', '2025-10-26 05:43:55'),
(89, 'Chuyên đề học tập Lịch sử 10 - Kết nối tri thức với cuộc sống', 'Sách lớp 10', 10000, 'public/image/book_20251026_054459_a79d0a.png', 'Sách chuyên đề học tập Lịch sử lớp 10 thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức ch', '2025-10-26 05:45:28', '2025-10-26 05:45:28'),
(90, 'Âm nhạc 12 - Kết nối tri thức với cuộc sống', 'Sách lớp 12', 12000, 'public/image/book_20251026_054614_0be33a.jpg', 'Sách Âm nhạc lớp 12 thuộc bộ Kết nối tri thức với cuộc sống, giúp học sinh phát triển năng khiếu, ki', '2025-10-26 05:46:26', '2025-10-26 05:46:26'),
(93, 'Chuyên đề học tập Vật lí 12 - Kết nối tri thức với cuộc sống', 'Sách lớp 12', 12000, 'public/image/book_20251026_055428_41eeb5.png', 'Sách Chuyên đề học tập Vật lí lớp 12 thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức chu', '2025-10-26 05:54:37', '2025-10-26 05:54:37'),
(94, 'Toán 12 (Tập 2) - Kết nối tri thức với cuộc sống', 'Sách lớp 12', 10000, 'public/image/book_20251105_124249_d93ece.png', 'Sách Toán lớp 12 tập hai thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức và bài tập về toán học nâng cao cho học sinh trung học phổ thông.', '2025-11-05 12:44:38', '2025-11-05 12:44:38'),
(95, 'Toán 12 (Tập 1) - Kết nối tri thức với cuộc sống', 'Sách lớp 12', 10000, 'public/image/book_20251105_124459_111d0e.png', 'Sách Toán lớp 12 tập 1 thuộc bộ Kết nối tri thức với cuộc sống, cung cấp kiến thức và bài tập về toán học cho học sinh THPT, chuẩn bị cho kỳ thi tốt nghiệp và đại học.', '2025-11-05 12:45:05', '2025-11-05 12:45:05');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT 0,
  `cccd` varchar(12) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(6) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `pob` varchar(100) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `address` varchar(100) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci DEFAULT NULL,
  `point` int(11) NOT NULL DEFAULT 0,
  `token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `status`, `cccd`, `dob`, `gender`, `pob`, `address`, `point`, `token`, `created_at`, `updated_at`) VALUES
(15, 'Nguyễn Văn A', 's@gmail.com', '$2y$10$e0NRu7n9s1mXo5l3Zt8OeG8j1v6z5b9c4d2f1g0h3j4k5l6m7n8', 1, '123456789012', '2000-01-01', 'Nam', 'Hà Nội', '123 Đường ABC, Phường XYZ, Quận 1, TP.HCM', 100, NULL, '2025-10-01 12:00:00', '2025-10-01 12:00:00'),
(16, 'Trần Thị B', 'b@gmail.com', '$2y$10$e0NRu7n9s1mXo5l3Zt8OeG8j1v6z5b9c4d2f1g0h3j4k5l6m7n8', 1, '123456789013', '2000-01-01', 'Nữ', 'Hà Nội', '456 Đường DEF, Phường UVW, Quận 2, TP.HCM', 100, NULL, '2025-10-01 12:00:00', '2025-10-01 12:00:00');
--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_type_book` (`id_type_book`);

--
-- Chỉ mục cho bảng `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_seller` (`id_seller`);

--
-- Chỉ mục cho bảng `detail_cart`
--
ALTER TABLE `detail_cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_book` (`id_book`),
  ADD KEY `id_cart` (`id_cart`);

--
-- Chỉ mục cho bảng `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Chỉ mục cho bảng `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Chỉ mục cho bảng `type_books`
--
ALTER TABLE `type_books`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `book`
--
ALTER TABLE `book`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT cho bảng `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT cho bảng `detail_cart`
--
ALTER TABLE `detail_cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT cho bảng `images`
--
ALTER TABLE `images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT cho bảng `transaction`
--
ALTER TABLE `transaction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT cho bảng `type_books`
--
ALTER TABLE `type_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `book_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `book_ibfk_2` FOREIGN KEY (`id_type_book`) REFERENCES `type_books` (`id`);

--
-- Các ràng buộc cho bảng `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`id_seller`) REFERENCES `users` (`id`);

--
-- Các ràng buộc cho bảng `detail_cart`
--
ALTER TABLE `detail_cart`
  ADD CONSTRAINT `detail_cart_ibfk_1` FOREIGN KEY (`id_book`) REFERENCES `book` (`id`),
  ADD CONSTRAINT `detail_cart_ibfk_2` FOREIGN KEY (`id_cart`) REFERENCES `cart` (`id`);

--
-- Các ràng buộc cho bảng `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);

--
-- Các ràng buộc cho bảng `transaction`
--
ALTER TABLE `transaction`
  ADD CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
