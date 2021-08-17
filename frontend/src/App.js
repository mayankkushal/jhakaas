import "bootstrap/dist/css/bootstrap.min.css";
import jsonServerProvider from "ra-data-json-server";
import React from "react";
import { Admin, Resource } from "react-admin";
import "./App.css";
import authProvider from "./auth/authProvider";
import { UserList } from "./component/users/List";

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

const dataProvider = jsonServerProvider("http://localhost:8000");
const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource name="users" list={UserList} />
  </Admin>
);

export default App;
