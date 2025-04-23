# 使用 Python 基礎鏡像
FROM python:3.10

# 設置工作目錄
WORKDIR /root/app

# 複製所有項目文件
COPY . .

# 聲明容器要使用的端口
EXPOSE 8001

# 創建輸出目錄
RUN mkdir -p output

# 設置 Python 不要生成 .pyc 文件和緩衝輸出
ENV PYTHONUNBUFFERED=1

# 創建啟動腳本
RUN echo '#!/bin/bash\n\
\n\
VENV_PATH="/root/app/venv"\n\
\n\
echo "檢查虛擬環境..."\n\
if [ ! -d "$VENV_PATH" ]; then\n\
    echo "創建虛擬環境..."\n\
    python -m venv $VENV_PATH\n\
fi\n\
\n\
# 激活虛擬環境\n\
source $VENV_PATH/bin/activate\n\
\n\
echo "安裝 Python 依賴..."\n\
pip install -r requirements.txt\n\
\n\
echo "安裝 Playwright..."\n\
playwright install\n\
playwright install-deps\n\
\n\
echo "啟動應用程序..."\n\
exec uvicorn app:app --host 0.0.0.0 --port 8001 --workers 1 --log-level info\n\
' > /start.sh \
    && chmod +x /start.sh

# 啟動命令
CMD ["/start.sh"]


