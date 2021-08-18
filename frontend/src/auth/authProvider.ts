import { AUTH_CHECK, AUTH_ERROR, AUTH_LOGIN, AUTH_LOGOUT } from "react-admin";
import auth from "./auth";

export default async (type: any, params: any) => {
  // called when the user attempts to log in
  if (type === AUTH_LOGIN) {
    const { username, password } = params;
    const data = await auth.login(username, password);
    console.log(data);
    return Promise.resolve();
  }
  // called when the user clicks on the logout button
  if (type === AUTH_LOGOUT) {
    localStorage.removeItem("token");
    localStorage.removeItem("permissions");
    return Promise.resolve();
  }
  // called when the API returns an error
  if (type === AUTH_ERROR) {
    const { status } = params;
    if (status === 401 || status === 403) {
      localStorage.removeItem("token");
      return Promise.reject();
    }
    return Promise.resolve();
  }
  // called when the user navigates to a new location
  if (type === AUTH_CHECK) {
    return localStorage.getItem("token") ? Promise.resolve() : Promise.reject();
  }
  return Promise.reject("Unknown method");
};
