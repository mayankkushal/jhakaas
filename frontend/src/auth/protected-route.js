import React from "react";
import { Route } from "react-router-dom";
import { Landing } from "../pages/Landing";
import auth from "./auth";

// ProtectedRoute template to define any new protected routes
export const ProtectedRoute = ({ component: Component, ...rest }) => {
  return (
    <Route
      {...rest}
      render={(props) => {
        // Goto the concerned route when authenticated
        if (auth.isAuthenticated()) {
          return <Component {...props} />;
        }
        // Goto the default login page when not authenticated
        else {
          return (
            <div>
              <Landing {...props} />
            </div>
          );
        }
      }}
    />
  );
};
