import axios from 'axios'

const Api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 30000,
})

Api.interceptors.response.use(
  (res) => res,
  (err) => {
    return Promise.reject(err.response ? err.response.data : { error: err.message })
  }
)

export default Api
