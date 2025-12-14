FROM python:alpine

# 设置环境变量
# PYTHONDONTWRITEBYTECODE: 防止生成 .pyc 文件
# PYTHONUNBUFFERED: 确保日志直接输出到控制台
# TZ: 设置时区
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖 (tzdata) 并设置时区
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# 复制依赖文件并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY main.py .

# 暴露应用端口
EXPOSE 3005

# 启动应用程序
CMD ["python", "main.py"]
