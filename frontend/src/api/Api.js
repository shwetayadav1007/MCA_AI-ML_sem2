import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || ''

const Api = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

Api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    return Promise.reject(err.response ? err.response.data : { error: err.message })
  }
)

export default Api
