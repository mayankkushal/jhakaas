import FilterDramaOutlinedIcon from '@material-ui/icons/FilterDramaOutlined'
import PeopleOutlineOutlinedIcon from '@material-ui/icons/PeopleOutlineOutlined'
import StorageOutlinedIcon from '@material-ui/icons/StorageOutlined'
import 'bootstrap/dist/css/bootstrap.min.css'
import React from 'react'
import { Admin, Resource } from 'react-admin'
import './App.css'
import authProvider from './auth/authProvider'
import { CloudFunctionCreate } from './component/cloudFunction/Create'
import { CloudFunctionEdit } from './component/cloudFunction/Edit'
import { CloudFunctionList } from './component/cloudFunction/List'
import { CollectionEdit } from './component/database/Edit'
import { CollectionList } from './component/database/List'
import { UserCreate } from './component/users/Create'
import { UserEdit } from './component/users/Edit'
import { UserList } from './component/users/List'
import customRoutes from './customRoutes'
import { dataProvider } from './dataProvider'
import { theme } from './theme'

const App = () => (
  <Admin
    dataProvider={dataProvider}
    authProvider={authProvider}
    theme={theme}
    customRoutes={customRoutes}
  >
    <Resource
      name="auth/users"
      options={{ label: 'Users' }}
      list={UserList}
      edit={UserEdit}
      create={UserCreate}
      icon={PeopleOutlineOutlinedIcon}
    />
    <Resource
      name="collection"
      options={{ label: 'Database' }}
      list={CollectionList}
      edit={CollectionEdit}
      icon={StorageOutlinedIcon}
    />
    <Resource
      name="cloud_function"
      options={{ label: 'Cloud Function' }}
      list={CloudFunctionList}
      edit={CloudFunctionEdit}
      create={CloudFunctionCreate}
      icon={FilterDramaOutlinedIcon}
    />
  </Admin>
)

export default App
