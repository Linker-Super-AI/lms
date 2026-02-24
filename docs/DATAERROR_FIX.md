# DataError 保存错误修复

## ✅ 问题已修复

### 错误信息
```
DataError: (1406, "Data too long for column 'content' at row 1")
```

### 问题原因
课程内容字段（`content`）原本是 `TEXT` 类型，最大只能存储 **65,535 字节（约 64KB）**。

当课程内容包含：
- 大量文本
- 多张图片
- 复杂的 Editor.js JSON 数据

就会超过这个限制，导致保存失败。

### 解决方案
已将相关字段修改为 `LONGTEXT` 类型，最大可存储 **4,294,967,295 字节（约 4GB）**。

## 📊 修复详情

### 已修改的字段

| 表名 | 字段名 | 原类型 | 新类型 | 最大长度 |
|------|--------|--------|--------|----------|
| `tabCourse Lesson` | `content` | TEXT | LONGTEXT | 4,294,967,295 字节 |
| `tabLMS Course` | `description` | TEXT | LONGTEXT | 4,294,967,295 字节 |

### 字段大小对比

```
TEXT:       65,535 字节      ≈ 64 KB    ❌ 容易超限
LONGTEXT: 4,294,967,295 字节 ≈ 4 GB    ✅ 足够使用
```

## ✅ 现在可以保存的内容

修复后，您可以在课程中保存：

✅ **大量文本内容**
- 数万字的课程描述
- 完整的教程文档
- 详细的课时说明

✅ **富文本内容**
- Editor.js 的复杂 JSON 结构
- 多个段落、列表、表格
- 代码块、引用等格式

✅ **多媒体内容**
- 多张图片（通过 URL 引用）
- 视频嵌入代码
- 音频播放器代码

## 🔧 如何验证修复

### 方法1：直接保存测试
1. 编辑课程或课时内容
2. 添加大量文本或多张图片
3. 点击保存
4. ✅ 应该能够成功保存

### 方法2：查看数据库字段
```bash
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 mariadb <<'SQL'
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
AND TABLE_NAME = 'tabCourse Lesson'
AND COLUMN_NAME = 'content';
SQL
```

**预期输出：**
```
DATA_TYPE: longtext
CHARACTER_MAXIMUM_LENGTH: 4294967295
```

## 📝 技术细节

### MySQL/MariaDB 文本类型对比

| 类型 | 最大长度 | 实际使用 |
|------|----------|----------|
| TINYTEXT | 255 字节 | 很少使用 |
| TEXT | 65,535 字节 (64 KB) | 短文本 ⚠️ |
| MEDIUMTEXT | 16,777,215 字节 (16 MB) | 中等文本 |
| LONGTEXT | 4,294,967,295 字节 (4 GB) | 大文本 ✅ |

### 为什么选择 LONGTEXT

1. **足够大**：4GB 对于课程内容完全够用
2. **性能影响小**：只有实际使用的空间会被占用
3. **兼容性好**：所有 MySQL/MariaDB 版本都支持
4. **未来无忧**：不用担心内容增长导致再次超限

### 修改 SQL 命令

如果将来需要手动修改其他字段：

```sql
ALTER TABLE `表名` MODIFY COLUMN `字段名` LONGTEXT;
```

示例：
```sql
ALTER TABLE `tabCourse Lesson` MODIFY COLUMN `content` LONGTEXT;
```

## ⚠️ 注意事项

### 1. 性能考虑

虽然 LONGTEXT 可以存储 4GB，但建议：

- ✅ **文本内容**：无限制，放心使用
- ✅ **图片**：通过 URL 引用，不要直接 base64 编码存储
- ✅ **视频**：使用外部链接（YouTube、Vimeo等）
- ❌ **大文件**：不要直接存储在数据库，使用文件系统

### 2. 备份建议

数据库备份时，LONGTEXT 字段会占用更多空间：

```bash
# 备份数据库
docker compose -f docker-compose-prod.yml exec mariadb \
  mysqldump -u root -padmin \
  _28befd2a5cb08663 > backup_$(date +%Y%m%d).sql

# 压缩备份
gzip backup_$(date +%Y%m%d).sql
```

### 3. 编辑器使用

在编辑课程内容时：
- 使用 Markdown 格式（推荐）
- 或使用 Editor.js 富文本编辑器
- 避免直接粘贴 Word 文档（可能包含大量隐藏格式）

## 🔄 其他可能需要修改的字段

如果将来遇到类似错误，可能需要修改这些字段：

```sql
-- 课程简介
ALTER TABLE `tabLMS Course`
MODIFY COLUMN `short_introduction` LONGTEXT;

-- 课程评论
ALTER TABLE `tabLMS Course Review`
MODIFY COLUMN `review` LONGTEXT;

-- 讨论内容
ALTER TABLE `tabDiscussion`
MODIFY COLUMN `content` LONGTEXT;

-- 章节标题/说明
ALTER TABLE `tabCourse Chapter`
MODIFY COLUMN `title` VARCHAR(500);
```

## 📞 如果再次遇到类似错误

### 步骤1：查看错误日志
```bash
docker compose -f docker-compose-prod.yml logs lms --tail=50 | grep DataError
```

### 步骤2：确认是哪个字段
错误信息会显示：
```
Data too long for column 'XXXX' at row 1
```

### 步骤3：修改字段类型
```bash
docker compose -f docker-compose-prod.yml exec lms \
  bench --site 192.168.20.118 mariadb <<'SQL'
ALTER TABLE `表名` MODIFY COLUMN `字段名` LONGTEXT;
SQL
```

### 步骤4：重试保存
刷新页面，重新保存内容。

## ✅ 总结

| 项目 | 状态 |
|------|------|
| 问题识别 | ✅ 完成 |
| 字段修改 | ✅ 完成 |
| 测试验证 | ✅ 完成 |
| 文档记录 | ✅ 完成 |

**现在可以放心地保存大量课程内容了！** 🎉

如果再遇到 DataError，参考本文档快速解决。
