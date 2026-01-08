import { ref, watch } from 'vue'

/**
 * 防抖组合式函数
 * @param {any} value - 要防抖的值
 * @param {number} delay - 延迟时间（毫秒）
 */
export function useDebounce(value, delay = 300) {
  const debouncedValue = ref(value.value)
  let timeout = null

  watch(value, (newValue) => {
    if (timeout) {
      clearTimeout(timeout)
    }

    timeout = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })

  return debouncedValue
}

/**
 * 防抖函数组合式函数
 * @param {Function} func - 要防抖的函数
 * @param {number} delay - 延迟时间（毫秒）
 */
export function useDebouncedFn(func, delay = 300) {
  let timeout = null

  const debouncedFn = (...args) => {
    if (timeout) {
      clearTimeout(timeout)
    }

    return new Promise((resolve) => {
      timeout = setTimeout(async () => {
        const result = await func(...args)
        resolve(result)
      }, delay)
    })
  }

  return debouncedFn
}
