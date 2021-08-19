import * as React from "react";
import { Route } from "react-router-dom";
import DataEditView from "./component/database/data/Edit";
import DataListView from "./component/database/data/List";

export default [
  <Route exact path="/collection/:id/show" component={DataListView} />,
  <Route exact path="/collection/:id/data/:data_id" component={DataEditView} />,
];
