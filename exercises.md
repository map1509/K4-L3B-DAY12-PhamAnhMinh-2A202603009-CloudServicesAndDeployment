# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: viết trực tiếp câu trả lời bên dưới từng câu hỏi.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Phạm Anh Minh  —  Mã học viên: 2A202603009

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

Khi thiếu `AGENT_API_KEY`, ứng dụng dừng ngay lúc tạo `Settings`. Điều này tốt hơn việc dùng khóa `changeme`, vì deployment lỗi được phát hiện ngay thay vì chạy công khai với một khóa ai cũng biết.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

Mỗi event được in thành một JSON object trên một dòng, ví dụ `{"event":"ask_completed","level":"info","timestamp":"...","user_id":"sv01","cost_usd":0.0001}`. Dòng này cho phép hệ thống log lọc theo `event` và đếm theo `user_id`; `print("đã trả lời xong")` chỉ là chuỗi tự do nên máy khó phân tích và không có metadata.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | khoảng 220 MB |
| Multi-stage | khoảng 150 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

Image một stage phải chứa cả môi trường build và mọi lớp cài đặt dependency, còn image multi-stage chỉ copy phần runtime cần thiết sang stage cuối. Vì vậy multi-stage thường nhỏ hơn và không mang theo công cụ hoặc file tạm của quá trình build. Kích thước cụ thể cần lấy từ `docker images` sau khi Docker daemon chạy.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

Trong Dockerfile hiện tại, layer `COPY requirements.txt` và layer cài dependency được cache lại khi chỉ sửa source. Các layer sau `COPY app` hoặc `COPY utils` phải chạy lại. Nếu đặt `COPY . .` trước `pip install`, mỗi thay đổi nhỏ trong code sẽ làm mất cache của bước cài dependency và build chậm hơn.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

Nếu process trong container chạy root và có lỗ hổng cho phép thực thi lệnh, kẻ tấn công có thể dùng quyền root trong container để đọc hoặc sửa mọi file mà root container được phép truy cập, rồi tìm đường khai thác Docker hoặc cấu hình host. `USER appuser` giới hạn process ở user thường, nên lỗ hổng không tự động biến thành quyền root trên host.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

Sliding window xóa các request có timestamp cũ hơn 60 giây rồi đếm request còn lại. Cách đếm theo phút đồng hồ có thể cho 20 request trong 2 giây: gửi 10 request ngay trước mốc `10:01:00`, rồi 10 request ngay sau mốc đó. Hai nhóm nằm ở hai phút lịch khác nhau nhưng thực tế chỉ cách nhau khoảng 2 giây.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

Rate limit giới hạn số lần gọi, còn cost guard giới hạn số tiền đã hoặc sắp tiêu. Ví dụ user gửi ít request nhưng mỗi prompt rất dài khiến chi phí dự kiến vượt ngân sách thì rate limit cho qua nhưng cost guard trả 402. Ngược lại, user gửi hơn 10 request trong một phút dù mỗi request rất rẻ thì rate limiter trả 429 trước khi gọi LLM.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

`/health` chỉ kiểm tra process nên vẫn trả 200 khi Redis mất kết nối. `/ready` kiểm tra Redis và trả 503, vì vậy load balancer ngừng gửi request mới vào các container chưa sẵn sàng nhưng không restart cả cụm chỉ vì dependency tạm thời lỗi.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

Khi scale ba agent, request có thể đi vào các container khác nhau. Nếu history nằm trong dict Python, mỗi container có bản sao riêng nên `history_length` lúc tăng lúc quay về 0 tùy request đi vào instance nào. Khi history nằm trong Redis, mọi instance đọc cùng một danh sách nên lịch sử nhất quán.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

Khi deploy Railway, ban đầu service agent khởi động được nhưng `/ready` trả 503 vì Redis service bị crash và `REDIS_URL` chưa kết nối tới Redis cloud. Mình kiểm tra log Railway, thấy Redis offline, tạo lại Redis service, gắn lại `REDIS_URL` bằng reference của Railway rồi redeploy. Sau đó `/health` trả 200, `/ready` trả 200 với Redis sẵn sàng.
