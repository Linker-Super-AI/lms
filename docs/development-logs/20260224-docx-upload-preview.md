# DOCX 文件上传与预览功能 - 开发记录

## 基本信息
- **开发时间：** 2026-02-24
- **开发者：** Claude + 用户
- **分支：** （待创建）
- **状态：** ✅ 已完成开发，待测试

## 需求说明

### 问题描述
系统目前的 Upload 功能不支持 DOCX 文件类型的上传和预览。用户需要能够上传 Word 文档（.docx）并在课程内容中预览。

### 功能需求
1. 支持 DOCX 文件上传
2. 提供文档预览功能（小文件）
3. 对于大文件或复杂格式，提供下载选项
4. 与现有 PDF、图片、视频等文件类型保持一致的用户体验

## 技术方案

### 设计思路
参考现有 PDF 上传和预览的实现方式，为 DOCX 文件添加类似功能。

**方案选择：**
经过调研，考虑了以下几种方案：
1. ❌ **Microsoft Office Online Viewer** - 需要公网访问，商业使用许可不明确，有隐私问题
2. ❌ **Google Docs Viewer** - 依赖外部服务，隐私问题
3. ✅ **Mammoth.js + 下载降级（采用）** - 开源免费，支持私有部署，无隐私问题
4. ⚠️ **仅提供下载** - 最简单但用户体验较差

**选择理由：**
- Mammoth.js 是开源库，完全免费
- 纯前端实现，不依赖外部服务
- 支持私有部署环境
- 对于简单的教学文档，转换效果足够好
- 大文件或复杂格式可以降级到下载

### 核心技术
- **Mammoth.js** (v1.8.0+): 将 DOCX 转换为 HTML 的 JavaScript 库
- **Vue 3 Composition API**: 用于组件开发
- **frappe-ui**: 保持 UI 风格一致性

### 涉及文件
1. `frontend/package.json` - 添加 mammoth 依赖
2. `frontend/src/components/DocxBlock.vue` - 新建 DOCX 预览组件
3. `frontend/src/components/UploadPlugin.vue` - 修改文件类型允许列表
4. `frontend/src/utils/upload.js` - 添加 DOCX 渲染逻辑

## 实现细节

### 1. 添加依赖

**文件：** `frontend/package.json`

```json
{
  "dependencies": {
    "mammoth": "^1.8.0",
    // ... 其他依赖
  }
}
```

### 2. 创建 DocxBlock 组件

**文件：** `frontend/src/components/DocxBlock.vue`

**功能特性：**
- 加载状态显示（加载中动画）
- 错误处理（加载失败提示）
- 文件大小检测（>2MB 直接下载）
- HTML 内容渲染（Mammoth.js 转换）
- 下载按钮（所有状态都可下载）
- 样式美化（标题、列表、表格等）

**核心逻辑：**
```javascript
const loadDocx = async () => {
  try {
    // 1. 获取文件
    const response = await fetch(props.file)

    // 2. 检查文件大小（>2MB 降级到下载）
    const contentLength = response.headers.get('content-length')
    if (contentLength && parseInt(contentLength) > 2 * 1024 * 1024) {
      shouldDownload.value = true
      return
    }

    // 3. 转换为 ArrayBuffer
    const arrayBuffer = await response.arrayBuffer()

    // 4. 使用 Mammoth 转换为 HTML
    const result = await mammoth.convertToHtml({ arrayBuffer })
    htmlContent.value = result.value
  } catch (err) {
    error.value = '文档预览失败，请下载后查看'
  }
}
```

**样式处理：**
- 标题（h1-h3）：不同字号和字重
- 段落：适当的行高和间距
- 列表：缩进和间距
- 表格：边框和背景色
- 图片：响应式宽度
- 代码：背景色和等宽字体

### 3. 修改文件类型允许

**文件：** `frontend/src/components/UploadPlugin.vue`

```vue
<!-- 允许的文件类型 -->
<FileUploader
  :fileTypes="['image/*', 'video/*', 'audio/*', '.pdf', '.docx']"
/>
```

```javascript
// 验证逻辑
const validateFile = (file) => {
  let extension = file.name.split('.').pop().toLowerCase()
  if (!['jpg', 'jpeg', 'png', 'mp4', 'mov', 'mp3', 'pdf', 'docx'].includes(extension)) {
    return 'Only image, video, audio, PDF and DOCX files are allowed.'
  }
}
```

### 4. 添加 DOCX 渲染逻辑

**文件：** `frontend/src/utils/upload.js`

```javascript
// 导入 DocxBlock 组件
import DocxBlock from '@/components/DocxBlock.vue'

// 在 renderFile 方法中添加 DOCX 处理
renderFile(file) {
  // ... 其他文件类型

  else if (this.isDocx(file.file_type)) {
    const app = createApp(DocxBlock, {
      file: window.location.origin + file.file_url,
    })
    app.mount(this.wrapper)
    return
  }

  // ...
}

// 添加 DOCX 类型判断方法
isDocx(type) {
  return ['docx', 'doc'].includes(type.toLowerCase())
}
```

## 用户体验流程

### 上传流程
1. 用户点击 Upload 按钮
2. 选择 DOCX 文件（文件选择器会显示 .docx 可选）
3. 文件上传到服务器
4. 系统自动识别为 DOCX 类型并渲染

### 预览流程

**小文件（≤2MB）：**
1. 显示加载动画
2. Mammoth.js 在前端转换为 HTML
3. 显示文档内容 + 下载按钮
4. 内容区域可滚动查看

**大文件（>2MB）：**
1. 检测到文件过大
2. 直接显示下载卡片
3. 提示"文件较大，建议下载后查看"
4. 提供下载按钮

**加载失败：**
1. 捕获错误
2. 显示错误提示
3. 提供下载按钮作为降级方案

## 构建与部署

### 构建步骤

```bash
# 1. 进入容器
docker exec lms-prod-lms-1 bash

# 2. 安装依赖
cd /home/frappe/frappe-bench/apps/lms/frontend
yarn add mammoth@^1.8.0

# 3. 构建前端
yarn build

# 4. 重启服务
exit
docker restart lms-prod-lms-1
```

### 部署结果
- ✅ Mammoth.js 依赖已安装（v1.11.0）
- ✅ 前端构建成功（14.01s）
- ✅ 服务重启完成

## 测试计划

### 测试内容
- [ ] 上传小型 DOCX 文件（< 2MB）
- [ ] 验证文档内容正确显示
- [ ] 测试各种格式（标题、列表、表格、图片）
- [ ] 上传大型 DOCX 文件（> 2MB）
- [ ] 验证自动降级到下载
- [ ] 测试下载功能
- [ ] 测试加载失败的错误处理
- [ ] 验证与 PDF、图片等其他文件类型共存

### 测试场景

#### 场景1：简单文档
- 文件：纯文字 + 简单格式
- 预期：正常转换并显示

#### 场景2：复杂格式
- 文件：包含标题、列表、表格、图片
- 预期：尽可能保留格式，无法转换的部分有提示

#### 场景3：大文件
- 文件：> 2MB 的 DOCX
- 预期：直接显示下载选项

#### 场景4：损坏文件
- 文件：损坏或无效的 DOCX
- 预期：显示错误提示 + 下载按钮

## 技术亮点

### 1. 智能降级策略
- 小文件：尝试预览
- 大文件：直接下载
- 失败：降级到下载

### 2. 用户体验优化
- 加载动画提示处理中
- 错误信息清晰明了
- 始终提供下载备选方案

### 3. 样式完善
- 自适应布局
- 美化的 HTML 内容显示
- 与系统整体风格一致

### 4. 性能考虑
- 文件大小检测避免浏览器卡顿
- 前端转换，不增加服务器负担
- 转换失败快速降级

## Mammoth.js 转换说明

### 支持的格式
- ✅ 标题（Heading 1-6）
- ✅ 段落
- ✅ 粗体、斜体
- ✅ 无序列表、有序列表
- ✅ 表格
- ✅ 图片
- ✅ 超链接
- ⚠️ 复杂样式（部分支持）
- ❌ 宏、脚本、嵌入对象

### 限制说明
- 不支持 .doc 格式（仅支持 .docx）
- 复杂的排版可能丢失部分样式
- 不支持修订、批注等协作功能
- 图表可能无法正确显示

### 最佳实践
建议上传的文档：
- 使用标准格式（标题、段落、列表）
- 避免复杂的页面布局
- 简化表格设计
- 图片以嵌入方式插入

## 遇到的问题

### 问题1：容器内安装依赖
- **问题描述：** 在宿主机上没有 yarn 命令
- **解决方案：** 使用 `docker exec` 在容器内执行命令

### 问题2：文件路径处理
- **问题描述：** 需要完整 URL 才能 fetch 文件
- **解决方案：** 在 upload.js 中添加 `window.location.origin` 前缀

## 后续优化建议

- [ ] 考虑添加 .doc 格式支持（需要额外库）
- [ ] 添加预览页面的打印功能
- [ ] 支持全屏查看文档
- [ ] 添加转换进度提示
- [ ] 缓存已转换的 HTML 内容
- [ ] 支持更多文档格式（如 RTF）

## 相关文档

- [Mammoth.js 官方文档](https://github.com/mwilliamson/mammoth.js)
- [PDF 上传实现参考](../IMAGE_UPLOAD_FIX.md)

## 代码提交

待测试通过后提交到 Git 仓库。

**提交信息建议：**
```
feat(upload): 添加 DOCX 文件上传和预览功能

- 添加 mammoth.js 依赖用于 DOCX 转 HTML
- 创建 DocxBlock.vue 组件实现文档预览
- 支持小文件预览和大文件下载降级
- 修改 UploadPlugin 和 upload.js 支持 DOCX 类型
```
