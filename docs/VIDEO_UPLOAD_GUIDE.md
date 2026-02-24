# 视频添加指南

## 📹 LMS 视频功能说明

### 架构层级
```
Course (课程)
  ├─ Chapter 1 (章节1)
  │   ├─ Lesson 1-1 (课时) ✅ 可添加视频
  │   ├─ Lesson 1-2 (课时) ✅ 可添加视频
  │   └─ Lesson 1-3 (课时) ✅ 可添加视频
  └─ Chapter 2 (章节2)
      ├─ Lesson 2-1 (课时) ✅ 可添加视频
      └─ Lesson 2-2 (课时) ✅ 可添加视频
```

**关键点：**
- ❌ Chapter（章节）本身不支持视频
- ✅ Lesson（课时）支持视频
- 💡 每个章节可以有多个课时，每个课时可以添加视频

---

## 🎯 添加视频的3种方法

### 方法1：YouTube 视频（推荐）⭐

**优点：**
- ✅ 免费托管
- ✅ 自动转码优化
- ✅ 自适应码率
- ✅ 全球 CDN 加速
- ✅ 无需担心带宽和存储

**步骤：**

#### 1. 上传视频到 YouTube

1. 访问 YouTube Studio: https://studio.youtube.com/
2. 点击「创建」→「上传视频」
3. 选择视频文件上传
4. 设置视频信息（标题、描述）
5. 选择可见性：
   - **公开**：所有人可见
   - **不公开**：仅有链接的人可见（推荐）
   - **私享**：仅指定用户可见
6. 点击「发布」

#### 2. 获取 YouTube 视频 URL

上传完成后，复制视频 URL，格式如下：
```
https://www.youtube.com/watch?v=VIDEO_ID
或
https://youtu.be/VIDEO_ID
```

#### 3. 在 LMS 中添加视频

**方式A：后台添加**

1. 访问课时编辑页面：
   ```
   http://192.168.20.118:8001/app/course-lesson/[lesson-name]
   ```

2. 找到「YouTube Video URL」字段

3. 粘贴 YouTube 链接：
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

4. 保存

**方式B：前端添加**

1. 访问课程页面
2. 点击「Edit Course」编辑课程
3. 选择章节和课时
4. 在「YouTube URL」字段粘贴链接
5. 保存

#### 示例效果

课时页面会自动嵌入 YouTube 播放器：
```
┌─────────────────────────────────────────┐
│  课时标题：第一课 - 入门介绍            │
├─────────────────────────────────────────┤
│                                         │
│         [YouTube 视频播放器]            │
│                                         │
│                                         │
├─────────────────────────────────────────┤
│  课程内容文本...                        │
└─────────────────────────────────────────┘
```

---

### 方法2：视频嵌入代码

**适用于：**
- Vimeo 视频
- Bilibili 视频
- 腾讯视频
- 自建视频服务器
- 其他视频平台

**步骤：**

#### 1. 获取视频嵌入代码

大多数视频平台提供嵌入代码（iframe），例如：

**Bilibili：**
```html
<iframe
  src="//player.bilibili.com/player.html?bvid=BV1xx411c7XZ"
  scrolling="no"
  border="0"
  frameborder="no"
  framespacing="0"
  allowfullscreen="true"
  width="100%"
  height="500">
</iframe>
```

**Vimeo：**
```html
<iframe
  src="https://player.vimeo.com/video/123456789"
  width="640"
  height="360"
  frameborder="0"
  allow="autoplay; fullscreen"
  allowfullscreen>
</iframe>
```

#### 2. 在课时内容中添加

1. 编辑课时内容（Course Lesson → Content）

2. 在 Markdown 或 HTML 编辑器中粘贴嵌入代码

3. 保存

#### 示例：Bilibili 视频

在课时内容中添加：
```markdown
# 第一课：入门教程

观看视频：

<iframe src="//player.bilibili.com/player.html?bvid=BV1xx411c7XZ"
  scrolling="no" border="0" frameborder="no"
  width="100%" height="500" allowfullscreen="true">
</iframe>

## 课程要点
1. 基础概念
2. 操作步骤
...
```

---

### 方法3：自己托管视频文件

**适用于：**
- 内部培训视频
- 不想依赖第三方平台
- 需要完全控制

**⚠️ 注意：不推荐直接上传大视频文件到数据库**

#### 推荐方案A：使用对象存储（S3/OSS）

1. **上传视频到对象存储**
   - 阿里云 OSS
   - 腾讯云 COS
   - AWS S3
   - MinIO（自建）

2. **获取视频 URL**
   ```
   https://your-bucket.oss-cn-beijing.aliyuncs.com/videos/lesson-01.mp4
   ```

3. **在课时内容中使用 video 标签**
   ```html
   <video width="100%" controls>
     <source src="https://your-bucket.oss-cn-beijing.aliyuncs.com/videos/lesson-01.mp4" type="video/mp4">
     您的浏览器不支持视频播放。
   </video>
   ```

#### 推荐方案B：使用文件服务器

1. **部署简单的文件服务器**
   ```bash
   # 在服务器上创建视频目录
   mkdir -p /home/services/lms/videos

   # 使用 nginx 提供静态文件服务
   # 或使用专门的视频 CDN
   ```

2. **上传视频文件**
   ```bash
   scp your-video.mp4 root@192.168.20.118:/home/services/lms/videos/
   ```

3. **配置 nginx 访问**
   在 nginx.conf 中添加：
   ```nginx
   location /videos {
       alias /home/services/lms/videos;
       add_header Access-Control-Allow-Origin *;
   }
   ```

4. **在课时中引用**
   ```html
   <video width="100%" controls>
     <source src="http://192.168.20.118:8001/videos/lesson-01.mp4" type="video/mp4">
   </video>
   ```

---

## 📋 完整示例：为每个章节添加视频

### 场景：课程有3个章节，每个章节需要1个视频

#### 步骤1：规划课程结构

```
课程：《Python 编程入门》
├─ 第一章：Python 基础
│   └─ 课时1.1：Python 环境搭建（视频）
├─ 第二章：数据类型
│   └─ 课时2.1：列表和字典（视频）
└─ 第三章：函数和模块
    └─ 课时3.1：函数定义（视频）
```

#### 步骤2：上传视频到 YouTube

1. 上传 3 个视频到 YouTube
2. 设置为「不公开」（仅限链接访问）
3. 获取 URL：
   - 视频1: `https://youtu.be/VIDEO_ID_1`
   - 视频2: `https://youtu.be/VIDEO_ID_2`
   - 视频3: `https://youtu.be/VIDEO_ID_3`

#### 步骤3：在 LMS 中创建课程结构

```bash
# 使用后台或脚本创建
http://192.168.20.118:8001/app/lms-course/uf67dh57kl
```

1. 创建章节1：「第一章：Python 基础」
2. 在章节1下创建课时1.1：「Python 环境搭建」
3. 在课时1.1的「YouTube Video URL」字段填入视频1链接
4. 重复步骤1-3创建其他章节和课时

#### 步骤4：测试

访问课程：
```
http://192.168.20.118:8001/courses/uf67dh57kl
```

点击课时，应该能看到嵌入的 YouTube 视频。

---

## 🎨 视频播放效果优化

### 1. 视频尺寸建议

| 用途 | 分辨率 | 宽高比 | 文件大小 |
|------|--------|--------|----------|
| 讲座/教程 | 1920x1080 | 16:9 | < 500MB |
| 演示视频 | 1280x720 | 16:9 | < 200MB |
| 简短说明 | 1280x720 | 16:9 | < 100MB |

### 2. 字幕支持

#### YouTube 字幕
YouTube 支持自动生成字幕，也可以上传自定义字幕：
1. 在 YouTube Studio 中打开视频
2. 左侧菜单选择「字幕」
3. 添加字幕语言
4. 上传 SRT 或 VTT 字幕文件

#### HTML5 视频字幕
```html
<video width="100%" controls>
  <source src="video.mp4" type="video/mp4">
  <track src="subtitles-zh.vtt" kind="subtitles" srclang="zh" label="中文">
  <track src="subtitles-en.vtt" kind="subtitles" srclang="en" label="English">
</video>
```

### 3. 视频封面

#### YouTube 缩略图
在 YouTube Studio 中自定义视频缩略图。

#### HTML5 视频封面
```html
<video width="100%" controls poster="thumbnail.jpg">
  <source src="video.mp4" type="video/mp4">
</video>
```

---

## ⚙️ 高级配置

### 1. 视频进度跟踪

LMS 支持跟踪学员的视频观看进度。YouTube 视频会自动跟踪。

### 2. 视频完成要求

可以设置学员必须观看完视频才能继续下一课时：

1. 编辑 LMS Settings
2. 启用「Prevent Skipping Videos」
3. 学员必须观看完整视频才能标记为完成

### 3. 视频加密和防盗链

#### YouTube 视频保护
- 设置为「不公开」
- 启用「嵌入限制」（仅特定域名）

#### 自托管视频保护
- 使用 HLS 加密
- 配置 nginx 防盗链
- 使用临时签名 URL

---

## 🚀 快速操作指南

### 为现有课程添加视频

```bash
# 1. 访问课程
http://192.168.20.118:8001/app/lms-course/uf67dh57kl

# 2. 编辑章节和课时
# 3. 在课时中添加 YouTube URL
# 4. 保存
```

### 批量添加视频（脚本）

如果有大量视频需要添加，可以使用脚本：

```python
import frappe

videos = [
    ("lesson-name-1", "https://youtu.be/VIDEO_ID_1"),
    ("lesson-name-2", "https://youtu.be/VIDEO_ID_2"),
    ("lesson-name-3", "https://youtu.be/VIDEO_ID_3"),
]

for lesson_name, youtube_url in videos:
    lesson = frappe.get_doc("Course Lesson", lesson_name)
    lesson.youtube = youtube_url
    lesson.save()
    print(f"✓ {lesson_name} - 视频已添加")

frappe.db.commit()
```

---

## ❓ 常见问题

### Q: 支持哪些视频格式？

**YouTube：** 支持所有常见格式（MP4, AVI, MOV, WMV 等），上传后自动转码

**自托管：** 推荐使用 MP4 (H.264 编码)

### Q: 视频大小限制？

**YouTube：**
- 免费账户：12小时，256GB
- 常规用户：15分钟（可验证后延长）

**自托管：**
- 取决于服务器存储和带宽
- 建议单个视频不超过 500MB

### Q: 视频加载慢怎么办？

**YouTube：**
- YouTube 有全球 CDN，通常很快
- 中国大陆可能需要科学上网

**自托管：**
- 使用 CDN 加速
- 压缩视频文件
- 使用自适应码率

### Q: 可以添加多个视频到一个课时吗？

可以！在课时内容中使用 iframe 或 video 标签添加多个视频：

```markdown
# 课时标题

## 视频1：介绍
<iframe src="youtube-video-1"></iframe>

## 视频2：演示
<iframe src="youtube-video-2"></iframe>
```

### Q: 视频不显示怎么办？

**检查清单：**
1. YouTube URL 是否正确
2. 视频是否设置为「私享」（改为「不公开」）
3. 浏览器是否屏蔽了 iframe
4. nginx 配置是否正确
5. 查看浏览器控制台错误信息

### Q: 支持直播吗？

支持！使用 YouTube 直播或其他平台的直播嵌入代码：

```html
<iframe
  src="https://www.youtube.com/embed/live_stream?channel=CHANNEL_ID"
  width="100%"
  height="500"
  allowfullscreen>
</iframe>
```

---

## 📊 视频方案对比

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **YouTube** | 免费、稳定、全球CDN | 需要科学上网（国内） | 公开课程、国际课程 |
| **Bilibili** | 国内访问快 | 需要审核、有广告 | 国内课程 |
| **Vimeo** | 无广告、专业 | 收费、上传限制 | 企业培训 |
| **阿里云OSS** | 国内快、可控 | 需要付费、需要开发 | 内部培训 |
| **自建服务器** | 完全控制 | 需要维护、带宽成本高 | 小规模使用 |

---

## ✅ 推荐方案总结

### 对于公开课程
✅ 使用 **YouTube**（免费、稳定）

### 对于国内课程
✅ 使用 **Bilibili** 或 **腾讯视频**

### 对于企业内部培训
✅ 使用 **阿里云 OSS** + **视频点播服务**

### 对于小规模测试
✅ 使用 **YouTube（不公开）** 最简单

---

**开始添加视频，让您的课程更生动！** 🎬
