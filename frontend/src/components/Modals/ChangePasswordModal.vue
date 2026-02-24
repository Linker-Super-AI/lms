<template>
	<Dialog
		v-model="show"
		:options="{
			title: '修改密码',
			size: 'lg',
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<FormControl
					type="password"
					label="当前密码"
					v-model="oldPassword"
					:error="errors.oldPassword"
					placeholder="请输入当前密码"
				/>
				<FormControl
					type="password"
					label="新密码"
					v-model="newPassword"
					:error="errors.newPassword"
					placeholder="至少8个字符"
				/>
				<FormControl
					type="password"
					label="确认新密码"
					v-model="confirmPassword"
					:error="errors.confirmPassword"
					placeholder="请再次输入新密码"
				/>
				<div v-if="errorMessage" class="text-sm text-red-600">
					{{ errorMessage }}
				</div>
			</div>
		</template>
		<template #actions>
			<Button @click="handleCancel" variant="subtle">取消</Button>
			<Button
				@click="handleSubmit"
				variant="solid"
				:loading="isSubmitting"
			>
				确认修改
			</Button>
		</template>
	</Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, FormControl, Button, toast, call } from 'frappe-ui'

const props = defineProps({
	modelValue: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(['update:modelValue'])

const show = ref(props.modelValue)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const isSubmitting = ref(false)
const errorMessage = ref('')
const errors = ref({
	oldPassword: '',
	newPassword: '',
	confirmPassword: '',
})

watch(
	() => props.modelValue,
	(value) => {
		show.value = value
	}
)

watch(show, (value) => {
	if (!value) {
		emit('update:modelValue', false)
		resetForm()
	}
})

const resetForm = () => {
	oldPassword.value = ''
	newPassword.value = ''
	confirmPassword.value = ''
	errorMessage.value = ''
	errors.value = {
		oldPassword: '',
		newPassword: '',
		confirmPassword: '',
	}
}

const validateForm = () => {
	errors.value = {
		oldPassword: '',
		newPassword: '',
		confirmPassword: '',
	}
	errorMessage.value = ''

	let isValid = true

	if (!oldPassword.value) {
		errors.value.oldPassword = '请输入当前密码'
		isValid = false
	}

	if (!newPassword.value) {
		errors.value.newPassword = '请输入新密码'
		isValid = false
	} else if (newPassword.value.length < 8) {
		errors.value.newPassword = '新密码至少需要8个字符'
		isValid = false
	}

	if (!confirmPassword.value) {
		errors.value.confirmPassword = '请确认新密码'
		isValid = false
	} else if (newPassword.value !== confirmPassword.value) {
		errors.value.confirmPassword = '两次输入的密码不一致'
		isValid = false
	}

	if (oldPassword.value && newPassword.value && oldPassword.value === newPassword.value) {
		errors.value.newPassword = '新密码不能与当前密码相同'
		isValid = false
	}

	return isValid
}

const handleSubmit = async () => {
	if (!validateForm()) {
		return
	}

	isSubmitting.value = true
	errorMessage.value = ''

	try {
		await call('frappe.core.doctype.user.user.update_password', {
			old_password: oldPassword.value,
			new_password: newPassword.value,
		})

		toast.success('密码修改成功')
		show.value = false
	} catch (error) {
		console.error('Password change error:', error)

		// 处理错误信息
		if (error && error.messages && error.messages.length > 0) {
			errorMessage.value = error.messages[0]
		} else if (error && error.exception) {
			const errorText = error.exception.toLowerCase()
			if (errorText.includes('wrong password') || errorText.includes('incorrect password')) {
				errorMessage.value = '当前密码错误，请重新输入'
			} else {
				errorMessage.value = '密码修改失败，请稍后重试'
			}
		} else if (error && typeof error === 'string') {
			errorMessage.value = error
		} else {
			errorMessage.value = '密码修改失败，请稍后重试'
		}
	} finally {
		isSubmitting.value = false
	}
}

const handleCancel = () => {
	show.value = false
}
</script>
