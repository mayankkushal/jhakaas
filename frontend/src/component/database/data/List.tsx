import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import { keyBy } from 'lodash'
import React, { useState } from 'react'
import {
  Datagrid,
  DeleteButton,
  ListContextProvider,
  TextField,
  Title,
  useQuery,
} from 'react-admin'
import { useParams } from 'react-router'

export const DataList = () => {
  const [page, setPage] = useState(1)
  const perPage = 5
  const params: { id: string } = useParams()
  const query = useQuery({
    type: 'getList',
    resource: `collection/${params.id}/show`,
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
      <Datagrid rowClick="edit" resource={`collection/${params.id}/data`}>
        <TextField source="id" />
        <DeleteButton />
      </Datagrid>
    </ListContextProvider>
  )
}

const DataListView = () => (
  <Card>
    <Title title="Data List" />
    <CardContent>
      <DataList />
    </CardContent>
  </Card>
)

export default DataListView
