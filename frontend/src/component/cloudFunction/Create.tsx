import React from 'react'
import { BooleanInput, Create, SimpleForm, TextInput } from 'react-admin'

export const CloudFunctionCreate = (props: any) => {
  return (
    <Create warnWhenUnsavedChanges {...props}>
      <SimpleForm redirect="edit">
        <TextInput source="name" />
        <BooleanInput source="is_async" />
      </SimpleForm>
    </Create>
  )
}
