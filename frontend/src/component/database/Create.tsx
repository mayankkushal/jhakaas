import React from 'react'
import { BooleanInput, Create, SimpleForm, TextInput } from 'react-admin'

export const CollectionCreate = (props: any) => {
  return (
    <div>
      <Create redirect="edit" {...props}>
        <SimpleForm>
          <TextInput source="name" />
          <BooleanInput source="is_strict" />
        </SimpleForm>
      </Create>
    </div>
  )
}
