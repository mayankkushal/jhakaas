import * as React from 'react'
import {
  BooleanInput,
  Create,
  PasswordInput,
  SimpleForm,
  TextInput,
} from 'react-admin'

export const UserCreate = (props: any) => (
  <Create {...props}>
    <SimpleForm>
      <TextInput source="email" />
      <PasswordInput source="password" />
      <BooleanInput source="is_active" />
      <BooleanInput source="is_superuser" />
      <BooleanInput source="is_verified" />
      <TextInput source="firstName" />
      <TextInput source="lastName" />
    </SimpleForm>
  </Create>
)
