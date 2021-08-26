import 'bootstrap/dist/css/bootstrap.min.css'
import jsonServerProvider from 'ra-data-json-server'
import React from 'react'
import { Admin, fetchUtils, Resource } from 'react-admin'
import './App.css'
import authProvider from './auth/authProvider'
import { CollectionEdit } from './component/database/Edit'
import { CollectionList } from './component/database/List'
import { UserCreate } from './component/users/Create'
import { UserEdit } from './component/users/Edit'
import { UserList } from './component/users/List'
import customRoutes from './customRoutes'
import { theme } from './theme'

// function App() {
//   return (
//     // Router Code
//     <BrowserRouter>
//       <div  className="App">
//         <ProtectedRoute
//             path='/'
//             exact
//             strict
//             component = {Home}
//           />
//         {/* <Route
//             path='/anotherpage'
//             exact
//             strict
//             component = {AnotherPage}
//           /> */}
//        </div>
//     </BrowserRouter>
//   );
// };

const fetchJson = (url: string, options: any = {}) => {
  options.user = {
    authenticated: true,
    token: `Bearer ${localStorage.getItem('token')}`,
  }
  return fetchUtils.fetchJson(url, options)
}

const dataProvider = jsonServerProvider('http://0.0.0.0:8888', fetchJson)
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
    />
    <Resource
      name="collection"
      options={{ label: 'Database' }}
      list={CollectionList}
      edit={CollectionEdit}
    />
  </Admin>
)

export default App
