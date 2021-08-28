import React from 'react'
import { Datagrid, Filter, List, SearchInput, TextField } from 'react-admin'

const NameFilter = (props: any) => (
  <Filter {...props}>
    <SearchInput source="q" resettable alwaysOn />
  </Filter>
)

export const CloudFunctionList = (props: any) => (
  <List filters={<NameFilter />} {...props}>
    <Datagrid rowClick="edit">
      <TextField source="name" />
      <TextField source="id" />
    </Datagrid>
  </List>
)
