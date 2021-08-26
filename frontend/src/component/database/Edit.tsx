import { Modal, Typography } from '@material-ui/core'
import React from 'react'
import {
  BooleanInput,
  CreateButton,
  DeleteButton,
  Edit,
  SaveButton,
  ShowButton,
  SimpleForm,
  TextField,
  Toolbar,
  TopToolbar,
  useEditController,
} from 'react-admin'
import { Route, useParams } from 'react-router-dom'
import { useToolbarStyles } from '../../styles/toolbar'
import { FieldCreate } from './fields/Create'
import { FieldList } from './fields/List'

const Aside = ({ record }: { record?: any }) => {
  return (
    <div style={{ margin: '1em' }}>
      <Typography variant="h6">Fields</Typography>
      <FieldList record={record} />
    </div>
  )
}

const CollectionEditToolbar = (props: any) => {
  const classes = useToolbarStyles(props)
  return (
    <Toolbar {...props}>
      <div className={classes.defaultToolbar}>
        <SaveButton disabled={props.pristine} />
        <div>
          <DeleteButton {...props} />
          <CreateButton
            label="ADD FIELD"
            basePath={`/collection/${props.collection_id}/field`}
          />
        </div>
      </div>
    </Toolbar>
  )
}

const CollectionEditActions = ({
  basePath,
  data,
}: {
  basePath?: string
  data?: any
  resource?: any
}) => {
  const params: { id: string } = useParams()
  return (
    <TopToolbar>
      <ShowButton basePath={basePath} record={data} label="show data" />
      <CreateButton
        basePath={`/collection/${params.id}/data_add`}
        label="add data"
      />
    </TopToolbar>
  )
}

export const CollectionEdit = (props: any) => {
  const { record } = useEditController(props)
  const classes = useToolbarStyles()
  return (
    <div>
      <Edit
        actions={<CollectionEditActions />}
        {...props}
        aside={record && <Aside />}
        title={record?.name}
      >
        <SimpleForm
          toolbar={<CollectionEditToolbar collection_id={record?.id} />}
        >
          <TextField source="id" />
          <TextField source="name" />
          <BooleanInput source="is_strict" />
        </SimpleForm>
      </Edit>
      <Route
        path="/collection/:collection_id/field/create"
        render={() => (
          <Modal open aria-labelledby="Add Field" className={classes.modal}>
            <FieldCreate {...props} collection={record} />
          </Modal>
        )}
      />
    </div>
  )
}
