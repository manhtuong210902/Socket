# Socket: Tỷ lệ giá vàng Việt Nam

## Nội dung
Chương trình mô phỏng ứng dụng trực tuyến gồm một server và nhiều client. Server sẽ lưu trữ thông tin giá vàng giúp client có thể tra cứu. Mọi quá trình client đăng nhập, client đăng xuất, .... đều được thể hiện trên màn hình của server.

## Yêu cầu
### 1. Kết nối
- Ý nghĩa: Cho phép client kết nối đến server thông qua kết nối TCP
- Mở rộng: Cho phép client và server đặt tại các host khác nhau (cho phép client nhập IP của server để kết nối)
### 2. Quản lý kết nối
- Ý nghĩa: Khi client hoặc server mất kết nối đột ngột, không làm chương trình treo hay xảy ra lỗi
- Mở rộng: Nếu một client mất kết nối không làm ảnh hưởng đến các client khác.
### 3. Đăng nhập
- Client đăng nhập bằng cách gửi username, password cho server
- Server nhận thông tin username, password từ client và kiểm tra với thông tin đã lưu trữ tại server
### 4. Đăng kí
- Client đăng ký bằng cách gửi username, password cho server
- Server nhận thông tin username, password từ client và kiểm tra với thông tin đã lưu trữ tại server, nếu đã tồn tại, gửi thông báo đến client, yêu cầu đăng ký tài khoản khác
### 5.Tra cứu
- Ý nghĩa:
  - Cho phép Client tra cứu theo ngày, theo loại vàng (SJC Ha Noi, SJC HCM, PNJ SJC...)
  - Server có thể tự tạo ra dữ liệu mẫu (nếu không làm phần nâng cao)
- Mở rộng:
  - Server sẽ kết nối tới một website khác (third party APIs/Web services) để lấy thông tin (JSON hoặc HTML), sau đó rút trích thông tin và lưu trữ liệu dưới Server để phục vụ request của Client.
  - Có thể dùng thư viện để kết nối và gửi các HTTP request đến các 3rd party APIs/Web serivces này.
  - Server cập nhật thông tin liên tục 30 phút 1 lần của ngày hôm đó
- API: https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date
### 6. Quản lý cơ sở dữ liệu
- Sử dụng file cấu trúc: xml, json, sql, .... 
### 7. Thoát
- Client được phép gửi thông báo ngừng kết nối đến server
- Server có thể gửi thông báo ngừng kết nối đến tất cả client đang hoạt động
### 8. Giao diện
- Có thiết kế giao diện đồ họa cho chương trình (GUI)
## Link Demo
link: https://drive.google.com/file/d/1J7SOJo6XonWao6uVb5dWo17Ze0BCDzqu/view

