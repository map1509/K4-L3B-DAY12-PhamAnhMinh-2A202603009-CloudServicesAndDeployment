# Thông Tin Deploy — Checkpoint 5

> Chỉ ghi tên biến môi trường; không ghi giá trị API key hoặc password Redis.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Phạm Anh Minh |
| Mã học viên | 2A202603009 |
| Repo | https://github.com/map1509/K4-L3B-DAY12-PhamAnhMinh-2A202603009-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://day12-agent-production-8237.up.railway.app |
| Platform | Railway |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Cloud

Các biến đã được cấu hình trên service `day12-agent`:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | Railway tự gán |
| `AGENT_API_KEY` | ✅ | Secret trong Railway Variables |
| `REDIS_URL` | ✅ | Reference tới Redis service của Railway |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |

## Lệnh Kiểm Tra

```powershell
curl.exe -i https://day12-agent-production-8237.up.railway.app/health
curl.exe -i https://day12-agent-production-8237.up.railway.app/ready
curl.exe -i -X POST https://day12-agent-production-8237.up.railway.app/ask `
  -H "Content-Type: application/json" `
  -d '{"question":"Hello"}'
```

## Kết Quả Chạy Thật

- `/health`: HTTP 200, service trả trạng thái `ok`.
- `/ready`: HTTP 200, Redis trả trạng thái `true`.
- `/ask` không có API key: HTTP 401 Unauthorized.
- Container khởi động thành công trên Railway với Uvicorn bind `0.0.0.0` và port do Railway cấp.

## Ảnh Chụp Màn Hình

Đã chuẩn bị thư mục `screenshots/` để lưu bằng chứng:

- `screenshots/dashboard.png` — dashboard Railway.
- `screenshots/health.png` — kết quả gọi `/health`.

Không ghi giá trị `AGENT_API_KEY`, password Redis hoặc secret khác vào repository.
