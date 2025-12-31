import request from '@/utils/request'

// 下载题目导入模板
export const downloadImportTemplate = () => {
  return request({
    url: '/question/import/template/',
    method: 'get',
    responseType: 'blob'
  })
}

// 批量导入题目
export const importQuestions = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/question/import/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 导出题目
export const exportQuestions = (data) => {
  return request({
    url: '/question/export/',
    method: 'post',
    data,
    responseType: 'blob'
  })
}

// 导出错题本
export const exportMistakeQuestions = () => {
  return request({
    url: '/mistake/export/',
    method: 'post',
    responseType: 'blob'
  })
}