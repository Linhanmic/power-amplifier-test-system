import * as XLSX from 'xlsx'

/**
 * 导出数据到Excel文件
 * @param {Array} data - 要导出的数据数组
 * @param {Array} columns - 列配置数组，每项包含 { prop, label, width? }
 * @param {String} filename - 文件名
 */
export function exportToExcel(data, columns, filename = 'export') {
  // 准备表头
  const headers = columns.map(col => col.label)

  // 准备数据行
  const rows = data.map(row => {
    return columns.map(col => {
      const value = row[col.prop]
      // 处理嵌套对象
      if (col.formatter) {
        return col.formatter(value, row)
      }
      return value !== null && value !== undefined ? value : ''
    })
  })

  // 合并表头和数据
  const sheetData = [headers, ...rows]

  // 创建工作表
  const ws = XLSX.utils.aoa_to_sheet(sheetData)

  // 设置列宽
  const colWidths = columns.map(col => ({
    wch: col.width || 15
  }))
  ws['!cols'] = colWidths

  // 创建工作簿
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')

  // 导出文件
  XLSX.writeFile(wb, `${filename}.xlsx`)
}

/**
 * 格式化日期时间
 */
export function formatDateTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * 状态文本映射
 */
export const statusMap = {
  draft: '草稿',
  reviewing: '评审中',
  approved: '已通过',
  rejected: '已拒绝',
  ready: '就绪',
  deprecated: '已废弃',
  active: '启用',
  inactive: '停用'
}

/**
 * 优先级文本映射
 */
export const priorityMap = {
  S: 'S',
  A: 'A',
  B: 'B',
  C: 'C'
}
