FROM n8nio/n8n:latest

USER root

# نصب Python + pip
RUN apk add --no-cache \
    python3 \
    py3-pip

# ساخت virtual environment
RUN python3 -m venv /opt/venv

# فعال‌سازی venv و نصب کتابخونه‌ها
RUN /opt/venv/bin/pip install --no-cache-dir \
    selenium \
    beautifulsoup4 \
    pandas \
    webdriver-manager \
    googlesearch-python \
    requests \
    "docling[all]"

# تنظیم PATH برای استفاده از venv
ENV PATH="/opt/venv/bin:$PATH"

# برگرد به کاربر n8n
USER node

# کپی فایل‌ها
COPY local_files /files