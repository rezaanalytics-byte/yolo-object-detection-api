# استفاده از ایمیج سبک پایتون
FROM python:3.11-slim

# تنظیم متغیرهای محیطی برای جلوگیری از کش شدن و بهینه‌سازی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تنظیم دایرکتوری کاری
WORKDIR /app

# نصب وابستگی‌های سیستمی مورد نیاز OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# کپی کردن فایل requirements و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# کپی کردن کد برنامه
COPY app.py .

# باز کردن پورت 8000
EXPOSE 8000

# دستور اجرای برنامه
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]