FROM python:slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装Python依赖
# 这一步会利用Docker缓存，只有requirements.txt变更时才会重新安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 设置时区为上海
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 创建非root用户
RUN useradd -m appuser

# 复制必要的文件
COPY main.py .

# 设置文件权限
RUN chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露应用端口
EXPOSE 3005

# 添加健康检查（使用根端点作为健康检查目标）
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import os, http.client; port = os.getenv('SERVER_PORT') or os.getenv('PORT') or '3005'; conn = http.client.HTTPConnection('localhost', int(port)); conn.request('GET', '/'); response = conn.getresponse(); exit(0 if response.status == 200 else 1)"

# 设置容器启动命令
CMD ["python", "main.py"]
