# Công Cụ Tìm Kiếm Nhanh (Search App)

Đây là ứng dụng web được xây dựng bằng Streamlit giúp bạn tìm kiếm nhanh các câu hỏi và đáp án từ các file dữ liệu.

## Tính năng
- 🔍 **Tìm kiếm nhanh chóng**: Gõ từ khóa và nhận ngay kết quả câu hỏi cùng đáp án đúng.
- 💬 **Hỗ trợ tiếng Việt**: Chức năng tìm kiếm bất chấp dấu câu, hỗ trợ tìm kiếm không dấu sát nghĩa.
- 🎨 **Giao diện hiện đại**: Thiết kế với phong cách tối giản, sử dụng thẻ card có hiệu ứng đẹp mắt cho kết quả tìm kiếm.

## Yêu cầu hệ thống
- Python 3.8+
- Các thư viện liệt kê trong `requirements.txt`

## Hướng dẫn định dạng dữ liệu
Ứng dụng sẽ tự động đọc toàn bộ các file `.csv` lưu trong cùng thư mục (được chuyển đổi cấu trúc từ file Excel). Cấu trúc sẽ yêu cầu các cột có tên như:
- `Phân loại` (Ghi: "Q" cho câu hỏi, "A" cho đáp án)
- `Câu hỏi` hoặc `Nội dung câu hỏi`
- `Đáp án` hoặc `Đáp án đúng` (Đánh dấu "X" hoặc "V" đối với đáp án đúng)

## Hướng dẫn cài đặt và sử dụng

1. **Cài đặt thư viện**:
   Mở Command Prompt/Terminal và chạy lệnh sau để cài đặt Streamlit:
   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy ứng dụng**:
   Sử dụng lệnh sau để khởi động App:
   ```bash
   streamlit run search_app.py
   ```

3. Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ `http://localhost:8501`.
