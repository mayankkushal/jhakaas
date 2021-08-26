import * as React from 'react'
import {
  BooleanField,
  Datagrid,
  EmailField,
  List,
  TextField,
} from 'react-admin'

export const UserList = (props: any) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <EmailField source="email" label="Email/Phone" />
      <BooleanField source="is_active" />
      <BooleanField source="is_superuser" />
      <BooleanField source="is_verified" />
      <TextField source="firstName" />
      <TextField source="lastName" />
    </Datagrid>
  </List>
)
