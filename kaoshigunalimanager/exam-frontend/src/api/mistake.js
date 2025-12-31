import request from '@/utils/request'

// 获取错题列表
export const getMistakeList = (params) => {
  return request({
    url: '/mistake/list',
    method: 'get',
    params
  })
}

// 获取错题统计
export const getMistakeStatistics = () => {
  return request({
    url: '/mistake/statistics',
    method: 'get'
  })
}

// 标记错题为已掌握
export const markMistakeAsMastered = (mistakeId) => {
  return request({
    url: `/mistake/${mistakeId}/mastered`,
    method: 'put'
  })
}