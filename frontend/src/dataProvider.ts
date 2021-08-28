import jsonServerProvider from 'ra-data-json-server'
import { fetchUtils } from 'react-admin'
import { API_URL } from './constants'

const fetchJson = (url: string, options: any = {}) => {
  options.user = {
    authenticated: true,
    token: `Bearer ${localStorage.getItem('token')}`,
  }
  return fetchUtils.fetchJson(url, options)
}

const baseDataProvider = jsonServerProvider(API_URL, fetchJson)

export const dataProvider = {
  ...baseDataProvider,
  runFunction: (resource: string) => {
    return fetchJson(`${API_URL}/${resource}`, { method: 'POST' }).then(
      ({ json }) => ({
        data: json,
      })
    )
  },
}
