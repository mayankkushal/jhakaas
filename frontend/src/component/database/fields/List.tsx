import keyBy from 'lodash/keyBy'
import React, { useState } from 'react'
import {
  BooleanField,
  Datagrid,
  DeleteButton,
  ListContextProvider,
  TextField,
  useQuery,
} from 'react-admin'

export const FieldList = ({ record }: { record: any }) => {
  const [page, setPage] = useState(1)
  const perPage = 50
  const query = useQuery({
    type: 'getList',
    resource: `collection/${record?.id}/fields`,
    payload: {
      pagination: { page, perPage },
      sort: { field: 'createdAt', order: 'DESC' },
    },
  })
  return (
    <ListContextProvider
      value={{
        ...query,
        data: keyBy(query.data, 'id'),
        ids: query.data?.map(({ id }: { id: any }) => id),
        page,
        perPage,
        setPage,
        resource: 'field',
        currentSort: { field: 'id', order: 'ASC' },
        selectedIds: [],
      }}
    >
      <Datagrid rowClick="edit" resource={`collection/${record?.id}/field`}>
        <TextField source="name" />
        <TextField source="type" />
        <BooleanField source="indexed" />
        <DeleteButton
          mutationMode={'pessimistic'}
          confirmTitle={'This change is irreversible'}
        />
      </Datagrid>
    </ListContextProvider>
  )
}
