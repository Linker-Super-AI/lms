<template>
	<div class="docx-block mb-4">
		<!-- 加载中状态 -->
		<div v-if="loading" class="flex items-center justify-center p-8 bg-surface-gray-1 rounded-lg">
			<div class="flex flex-col items-center space-y-3">
				<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-ink-gray-7"></div>
				<span class="text-sm text-ink-gray-7">正在加载文档...</span>
			</div>
		</div>

		<!-- 错误状态或大文件直接下载 -->
		<div
			v-else-if="error || shouldDownload"
			class="flex flex-col items-center justify-center p-8 bg-surface-gray-1 rounded-lg border border-gray-200"
		>
			<FileText class="w-12 h-12 text-ink-gray-6 mb-3" />
			<div class="text-center mb-4">
				<p class="text-sm text-ink-gray-7 mb-1" v-if="error">
					{{ error }}
				</p>
				<p class="text-sm text-ink-gray-7" v-else>
					文件较大，建议下载后查看
				</p>
				<p class="text-xs text-ink-gray-6 mt-1" v-if="fileName">
					{{ fileName }}
				</p>
			</div>
			<Button @click="downloadFile" variant="solid">
				<template #prefix>
					<Download class="w-4 h-4" />
				</template>
				下载文档
			</Button>
		</div>

		<!-- 文档预览内容 -->
		<div v-else class="docx-content-wrapper">
			<div class="flex items-center justify-between p-3 bg-surface-gray-1 rounded-t-lg border border-b-0 border-gray-200">
				<div class="flex items-center space-x-2">
					<FileText class="w-5 h-5 text-ink-gray-7" />
					<span class="text-sm font-medium text-ink-gray-8">{{ fileName || '文档预览' }}</span>
				</div>
				<Button @click="downloadFile" variant="subtle" size="sm">
					<template #prefix>
						<Download class="w-4 h-4" />
					</template>
					下载
				</Button>
			</div>
			<div
				class="docx-content p-6 bg-white rounded-b-lg border border-gray-200 overflow-auto"
				v-html="htmlContent"
			></div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mammoth from 'mammoth'
import { Button } from 'frappe-ui'
import { FileText, Download } from 'lucide-vue-next'

const loading = ref(true)
const error = ref(null)
const htmlContent = ref('')
const shouldDownload = ref(false)
const fileName = ref('')

const props = defineProps({
	file: {
		type: String,
		required: true,
	},
})

onMounted(async () => {
	await loadDocx()
})

const loadDocx = async () => {
	try {
		loading.value = true
		error.value = null

		// 提取文件名
		const urlParts = props.file.split('/')
		fileName.value = decodeURIComponent(urlParts[urlParts.length - 1])

		// 获取文件
		const response = await fetch(props.file)
		if (!response.ok) {
			throw new Error('无法加载文档文件')
		}

		// 检查文件大小（如果响应头中有）
		const contentLength = response.headers.get('content-length')
		if (contentLength && parseInt(contentLength) > 2 * 1024 * 1024) {
			// 大于 2MB
			shouldDownload.value = true
			loading.value = false
			return
		}

		// 转换为 ArrayBuffer
		const arrayBuffer = await response.arrayBuffer()

		// 使用 mammoth 转换
		const result = await mammoth.convertToHtml({ arrayBuffer })
		htmlContent.value = result.value

		// 如果有转换警告，可以在控制台显示
		if (result.messages.length > 0) {
			console.warn('DOCX 转换警告:', result.messages)
		}

		loading.value = false
	} catch (err) {
		console.error('加载 DOCX 文件失败:', err)
		error.value = '文档预览失败，请下载后查看'
		loading.value = false
	}
}

const downloadFile = () => {
	const link = document.createElement('a')
	link.href = props.file
	link.download = fileName.value || 'document.docx'
	document.body.appendChild(link)
	link.click()
	document.body.removeChild(link)
}
</script>

<style scoped>
.docx-content-wrapper {
	max-width: 100%;
}

.docx-content {
	max-height: 600px;
	line-height: 1.6;
}

/* 美化转换后的HTML内容 */
.docx-content :deep(p) {
	margin-bottom: 0.75rem;
}

.docx-content :deep(h1) {
	font-size: 1.875rem;
	font-weight: 700;
	margin-top: 1.5rem;
	margin-bottom: 1rem;
	color: theme('colors.gray.900');
}

.docx-content :deep(h2) {
	font-size: 1.5rem;
	font-weight: 600;
	margin-top: 1.25rem;
	margin-bottom: 0.875rem;
	color: theme('colors.gray.900');
}

.docx-content :deep(h3) {
	font-size: 1.25rem;
	font-weight: 600;
	margin-top: 1rem;
	margin-bottom: 0.75rem;
	color: theme('colors.gray.800');
}

.docx-content :deep(ul),
.docx-content :deep(ol) {
	margin-left: 1.5rem;
	margin-bottom: 0.75rem;
}

.docx-content :deep(li) {
	margin-bottom: 0.25rem;
}

.docx-content :deep(table) {
	width: 100%;
	border-collapse: collapse;
	margin-bottom: 1rem;
}

.docx-content :deep(table td),
.docx-content :deep(table th) {
	border: 1px solid theme('colors.gray.300');
	padding: 0.5rem;
}

.docx-content :deep(table th) {
	background-color: theme('colors.gray.100');
	font-weight: 600;
}

.docx-content :deep(img) {
	max-width: 100%;
	height: auto;
	margin: 1rem 0;
}

.docx-content :deep(strong) {
	font-weight: 600;
}

.docx-content :deep(em) {
	font-style: italic;
}

.docx-content :deep(code) {
	background-color: theme('colors.gray.100');
	padding: 0.125rem 0.25rem;
	border-radius: 0.25rem;
	font-family: monospace;
	font-size: 0.875em;
}
</style>
