# 图片上传显示问题修复

## ✅ 问题已修复

### 问题描述
在课程中上传图片后，图片无法显示（显示为加载中或404错误）。

### 原因分析
Nginx 配置中缺少 `/files` 路径的静态文件服务配置，导致用户上传的文件无法通过 HTTP 访问。

### 解决方案
已在 `/home/services/lms/docker/nginx.conf` 中添加文件访问配置：

```nginx
# 用户上传的文件（图片、文档等）
location ~ ^/files/(.*)$ {
    try_files /192.168.20.118/public/files/$1 /lms.localhost/public/files/$1 =404;
    root /home/frappe/frappe-bench/sites;
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

### 验证修复
1. 重启 nginx 服务已完成
2. 测试图片访问：
   ```bash
   curl -I http://192.168.20.118:8001/files/ScreenShot_2026-02-24_150201_685.png
   # 返回 HTTP/1.1 200 OK 表示成功
   ```

## 📸 如何在课程中上传图片

### 方法1：在课程内容编辑器中上传

1. **编辑课程或课时**
   ```
   访问：http://192.168.20.118:8001/app/course-lesson/[lesson-name]
   ```

2. **在内容编辑器中添加图片**
   - 点击编辑器工具栏的「插入图片」按钮
   - 或在 Markdown 内容中使用图片语法

3. **上传图片**
   - 点击「Upload」或「上传」
   - 选择本地图片文件
   - 等待上传完成

4. **图片会自动插入**
   - 格式：`![图片描述](/files/filename.png)`
   - 图片 URL：`http://192.168.20.118:8001/files/filename.png`

### 方法2：在文件管理器中上传

1. **访问文件管理器**
   ```
   http://192.168.20.118:8001/app/file
   ```

2. **点击「Upload」上传文件**

3. **复制文件 URL**
   - 打开上传的文件详情
   - 复制「File URL」
   - 在课程内容中使用这个 URL

### 方法3：直接在 Markdown 中使用

在课程内容中使用 Markdown 语法：

```markdown
![图片说明](/files/your-image.png)

或使用完整 URL：
![图片说明](http://192.168.20.118:8001/files/your-image.png)
```

## 📁 文件存储位置

### 容器内路径
```
/home/frappe/frappe-bench/sites/192.168.20.118/public/files/
```

### 宿主机路径（通过 Volume）
通过 Docker Volume `lms-sites` 存储：
```bash
docker volume inspect lms-prod_lms-sites
```

## 🔧 支持的文件类型

### 图片
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- SVG (.svg)
- WebP (.webp)

### 文档
- PDF (.pdf)
- Word (.doc, .docx)
- Excel (.xls, .xlsx)
- PowerPoint (.ppt, .pptx)

### 其他
- 文本文件 (.txt, .md)
- 压缩文件 (.zip, .rar)
- 音频 (.mp3, .wav)
- 视频 (.mp4, .webm) - 但建议使用专门的视频服务

## ⚙️ 上传限制

### 当前配置
```nginx
client_max_body_size 50m;
```

**单个文件最大：50 MB**

### 修改上传限制

如需增加上传文件大小限制，编辑 nginx 配置：

```bash
nano /home/services/lms/docker/nginx.conf

# 修改
client_max_body_size 100m;  # 改为 100MB

# 重启 nginx
docker compose -f docker-compose-prod.yml restart nginx
```

## 🖼️ 图片优化建议

### 1. 压缩图片
上传前使用工具压缩图片：
- TinyPNG (https://tinypng.com/)
- ImageOptim (Mac)
- Squoosh (https://squoosh.app/)

### 2. 合适的尺寸
- 课程封面：建议 1200x630 px
- 内容图片：建议宽度不超过 1200px
- 缩略图：建议 400x300 px

### 3. 格式选择
- 照片：使用 JPEG
- 图标/插图：使用 PNG
- 简单图形：使用 SVG
- 动画：使用 GIF 或 WebP

## ⚠️ 注意事项

1. **文件名规范**
   - 避免使用中文文件名
   - 使用小写字母、数字、下划线、连字符
   - 示例：`course_image_01.png`

2. **版权问题**
   - 确保有权使用上传的图片
   - 注明图片来源（如需要）

3. **备份**
   - 重要图片建议在本地保留备份
   - Docker Volume 已持久化存储

4. **缓存**
   - 图片已配置7天缓存
   - 如需立即更新，修改文件名重新上传

## 🐛 常见问题

### Q: 图片上传后显示破损图标？
A:
1. 检查图片格式是否支持
2. 清除浏览器缓存
3. 检查图片URL是否正确

### Q: 无法上传大文件？
A:
- 检查文件大小是否超过50MB
- 增大 `client_max_body_size` 限制

### Q: 图片URL显示404？
A:
- 确认 nginx 已重启
- 检查文件是否真的上传成功
- 查看 nginx 日志：`docker compose logs nginx`

### Q: 如何批量上传图片？
A:
1. 访问文件管理器：http://192.168.20.118:8001/app/file
2. 可以一次选择多个文件上传
3. 或使用 FTP/SFTP 直接上传到服务器文件夹

## 📊 检查上传的文件

### 查看所有已上传文件
```
http://192.168.20.118:8001/app/file
```

### 命令行查看
```bash
docker compose -f docker-compose-prod.yml exec lms \
  ls -lah /home/frappe/frappe-bench/sites/192.168.20.118/public/files/
```

### 测试文件访问
```bash
# 替换为实际文件名
curl -I http://192.168.20.118:8001/files/your-file-name.png
```

## 🎯 最佳实践

1. **统一命名规则**
   ```
   course-name_section-01_image-01.png
   chapter-02_diagram.svg
   lesson-05_screenshot.jpg
   ```

2. **组织文件夹**（如使用 FTP 上传）
   ```
   /files/
     /course-images/
     /lesson-screenshots/
     /diagrams/
   ```

3. **使用 CDN**（可选，高级用法）
   - 对于流量大的站点
   - 可配置 S3 或其他对象存储
   - 需要修改 Frappe 配置

---

**修复完成时间：** 2026-02-24
**Nginx 配置已更新，图片现在可以正常显示了！** ✅
