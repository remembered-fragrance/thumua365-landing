# thumua365-landing — trang giới thiệu THUMUA365

Một trang tĩnh: `index.html` (CSS nằm sẵn trong trang) + `main.js` + `config.js` + logo.
**Không build, không framework, không thư viện, không công cụ theo dõi.** Trang ~90 KB chưa nén (~22 KB khi máy chủ nén gzip), cộng ảnh WebP ~500 KB chỉ tải khi cuộn tới.
Lighthouse (máy local): Hiệu năng / Truy cập / Thực hành tốt / SEO = 100 cả mobile lẫn desktop.

| File | Là gì |
|---|---|
| `index.html` | Toàn bộ nội dung + CSS |
| `config.js` | **Chỗ duy nhất** chứa link APK và link bản web |
| `main.js` | Chuyển mục bằng lăn chuột / phím, chấm điều hướng, hiệu ứng khi vào mục, gắn link từ `config.js` |
| `logo.svg`, `apple-touch-icon.png`, `icon-512.png` | Chép từ `public/` của repo app |

Tắt JavaScript trang vẫn đọc được đủ: chữ hiện sẵn, nút web vẫn bấm được, cuộn bắt mục do CSS lo.

## Xem ở máy

```bash
python tools/xem-thu.py
```

Mở http://127.0.0.1:4173. Trong Claude Code đã có sẵn `.claude/launch.json` (tên `landing`).
Mở thẳng file `index.html` bằng trình duyệt cũng chạy.

## File APK

Trang đã viết sẵn như có app Android: hai nút "App Android · Tải file APK" trỏ tới
`tai/thumua365.apk`, phần Cách dùng và Hỏi đáp nói "tải file APK về cài".

**Trước khi deploy phải chép file thật vào `tai/thumua365.apk`.** Chưa có file thì bấm nút ra lỗi
không tìm thấy, và console có một lỗi 404. Có file rồi thì nút tự ghi kèm dung lượng
("Tải file APK · 24 MB").

Để file ở chỗ khác thì điền URL đầy đủ vào `apkUrl` trong `config.js` (khi đó nút không ghi dung
lượng). Để trống `''` thì nút đổi về "Sắp có" và bấm vào chỉ cuộn tới phần hỏi đáp; nhớ sửa lại
câu chữ ở phần Cách dùng và Hỏi đáp cho khớp.

Đổi địa chỉ bản web cũng ở `config.js` (`web`). Trong `index.html` vẫn ghi sẵn
`https://thumua365.id.vn` làm dự phòng khi JS chưa tải xong. Đổi domain thì tìm-thay luôn trong đó
cho chắc (câu chữ "thumua365.id.vn" trong phần Cách dùng và Hỏi đáp cũng vậy).

## Deploy

Đang chạy ở **https://thumua365-landing.vercel.app** (Vercel, project `thumua365-landing`, tài khoản
`remembered-fragrance`). Repo GitHub riêng tư `remembered-fragrance/thumua365-landing` đã nối với
Vercel: **push lên nhánh `main` là web tự cập nhật** sau vài giây. Push nhánh khác thì Vercel tạo
bản xem thử riêng (cần đăng nhập Vercel mới xem được).

Deploy tay từ máy (cần `vercel login` một lần; trên Windows PowerShell dùng `npx.cmd`):

```bash
npx vercel deploy --prod
```

`.vercelignore` loại `tools/`, `.claude/` và README khỏi web. Vercel tự nén gzip/brotli và đặt
`Cache-Control: max-age=0, must-revalidate`, nên sửa `config.js` xong deploy là người xem thấy ngay.

Gắn tên miền riêng: Vercel → project → Settings → Domains.

## Cách trang chuyển mục

- Màn ≥ 768px rộng và ≥ 600px cao: CSS `scroll-snap-type: y mandatory`, cộng `main.js` bắt lăn
  chuột để **mỗi lần lăn sang đúng một mục** (lăn liền tay hay quán tính touchpad cũng chỉ một mục).
- Điện thoại: `proximity` — vuốt tự nhiên, gần mép mục thì hít vào, không giật ngược.
- Mục cao hơn màn hình (bảng giá trên máy tính bảng, tính năng trên điện thoại): cuộn bình thường
  tới hết mục rồi mới sang mục kế.
- Phím ↑ ↓ PageUp PageDown Home End và chấm bên phải đều chuyển mục.
- `prefers-reduced-motion`: tắt mọi hiệu ứng, chuyển mục không trượt, chữ hiện ngay.

## Hoạ tiết nông sản

Trang đầu: vài chiếc lá trôi (thẻ `<i class="leaf">` trong mục `#dau`). Các mục sau mỗi mục **một**
loại, đặt bằng thuộc tính `data-crop` trên thẻ `<section>`:

| `data-crop` | Hình |
|---|---|
| `caphe` | Hạt cà phê |
| `tieu` | Chùm tiêu (màu theo `--cc` của mục: đỏ trên nền đất, xanh trên nền sáng) |
| `dieu` | Hạt điều |
| `lacaosu` | Lá cao su ba lá chét |
| `mu` | Giọt mủ cao su (trắng, hợp nền xanh) |

Đổi loại thì sửa `data-crop`; bỏ thuộc tính là mục đó không có hoạ tiết. Độ đậm từng mục là biến
`--o` trong CSS. `main.js` rải hình hai bên mép (6 hình trên máy tính, 4 trên điện thoại), vị trí cố
định theo từng mục. Hình chỉ trôi ở mục đang xem, và đứng yên khi bật giảm chuyển động.

## Ảnh thật

Mười bốn ảnh chụp thật (có thông tin máy ảnh, không phải ảnh AI) lấy từ Unsplash, dùng theo
[giấy phép Unsplash](https://unsplash.com/license): miễn phí cả thương mại, không bắt ghi tên. Trang
vẫn ghi tên tác giả ở chân trang. Ảnh đã cắt khung và nén WebP, nằm trong `img/`, và chỉ tải khi
sắp cuộn tới (`loading="lazy"`).

| File | Ảnh gốc | Tác giả, nơi chụp |
|---|---|---|
| `nen-ca-phe-*`, `hang-ca-phe` | [JqF4IS65xEg](https://unsplash.com/photos/JqF4IS65xEg) | Dang Cong, Đắk Nông |
| `so-sot-ca-phe` | [YpLkgbXjirI](https://unsplash.com/photos/YpLkgbXjirI) | Sara Hobbs, Đà Lạt |
| `the-vua` | [7K64kQrcsxU](https://unsplash.com/photos/7K64kQrcsxU) | Dang Cong, Đắk Nông |
| `hang-cao-su` | [I_40CRTRSBs](https://unsplash.com/photos/I_40CRTRSBs) | Isuru Ranasinha |
| `hang-ho-tieu` | [07mSvSqbij4](https://unsplash.com/photos/07mSvSqbij4) | Praswin Prakashan, Kerala |
| `hang-dieu` | [RRLJN_EvFbE](https://unsplash.com/photos/RRLJN_EvFbE) | Snehsha Tank |
| `so-xe-cho-hang` | [xA-qf1joVHE](https://unsplash.com/photos/xA-qf1joVHE) | Jimmy Art Devier (đã cắt bỏ biển số xe) |
| `the-nong-dan-hai-ca-phe` | [1-ZUhMFleK0](https://unsplash.com/photos/1-ZUhMFleK0) | Luba Glazunova |
| `so-so-tay` | [NqagKaulCyc](https://unsplash.com/photos/NqagKaulCyc) | Michał Lis |
| `so-may-tinh` | [0rHxkbcvQAE](https://unsplash.com/photos/0rHxkbcvQAE) | FIN |
| `so-can-hang` | [AEaNpTt2P3Y](https://unsplash.com/photos/AEaNpTt2P3Y) | Michael Starkie |
| `so-dien-thoai` | [rNFMDubIqqA](https://unsplash.com/photos/rNFMDubIqqA) | Leonardo Baldissara |
| `the-doanh-nghiep` | [4TDXpo3odG8](https://unsplash.com/photos/4TDXpo3odG8) | David Maillard |
| `nen-cao-su-*` | [gI2zE9HfVzE](https://unsplash.com/photos/gI2zE9HfVzE) | Monineath Horn, Campuchia |

Có ảnh chụp thật ở vựa, rẫy của mình thì thay vào đúng tên file là xong; nhớ sửa luôn dòng ghi tên ở
chân trang.

## Dải cảnh làng quê

Đáy bảy mục có một cảnh vẽ SVG, không chữ, kể đúng chuyện của mục: xe hàng vào vựa, xóm đêm sáng
đèn dưới trời sao, rẫy cao su có chén hứng mủ, cây điều và xe đạp chở điều, nhà nông dân – vựa –
công ty nối bằng con đường, mặt trời lên trên đồi, võng dưới gốc cây với ấm trà. Mục "Cách dùng" và
"Bắt đầu" dùng ảnh thật làm nền nên không có cảnh vẽ.

Cảnh **sinh bằng script**, đừng sửa tay trong `index.html`:

```bash
python tools/ve-canh.py index.html
```

Sửa hình, màu, vị trí trong `tools/ve-canh.py` rồi chạy lại; script tự xoá cảnh cũ trước khi chèn.
Chuyển động (xe chạy vào, sao lấp lánh, khói bếp, võng đung đưa, mặt trời lên) nằm ở CSS, chỉ chạy
ở mục đang xem và tắt hẳn khi bật giảm chuyển động.

## Nội dung

Giá, hạn mức gói miễn phí, 30 ngày dùng thử, "hết hạn không khoá sổ / không tự trừ tiền / hoàn tiền
7 ngày" chép đúng từ `src/config.ts` và `site/index.html` của repo app. **Đổi giá bên app thì sửa
cả ở đây** — trang này không tự đọc `config.ts`.

Không có số liệu người dùng hay lời chứng thực. Phiếu cà phê ở phần mở đầu ghi rõ "Số liệu ví dụ".

Trang điều khoản / quyền riêng tư nằm ở `site/` của repo app, chưa liên kết từ đây vì chưa rõ sẽ
xuất bản ở domain nào.
