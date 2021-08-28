import { Typography } from '@material-ui/core'
import React, { useState } from 'react'
import {
  BooleanInput,
  Button,
  Edit,
  SimpleForm,
  TextInput,
  useDataProvider,
} from 'react-admin'
import ReactJson from 'react-json-view'
import { CodeInput } from '../CodeInput'

const Aside = (props: any) => {
  const { record } = props
  const dataProvider = useDataProvider()
  const [data, setData] = useState<object | null | undefined>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<object | null>()

  const onClick = () => {
    setData(null)
    setError(null)
    setLoading(true)
    dataProvider
      .runFunction(`cloud_function/${record?.id}/run`)
      .then(({ data }: { data?: object }) => {
        setData(data)
        setLoading(false)
      })
      .catch((error: any) => {
        setError(error.body)
        setLoading(false)
      })
  }
  return (
    <div style={{ margin: '1em', width: '30%' }}>
      <Typography variant="h6">Execute</Typography>
      <div>
        {loading && <h6>Loading</h6>}
        {data && (
          <ReactJson src={data ?? {}} name={false} displayDataTypes={false} />
        )}
        {error && (
          <ReactJson
            src={error ?? {}}
            name={false}
            displayDataTypes={false}
            displayObjectSize={false}
          />
        )}
      </div>
      <Button label="Run" onClick={onClick} disabled={!record?.code} />
    </div>
  )
}

export const CloudFunctionEdit = (props: any) => {
  return (
    <Edit aside={<Aside />} warnWhenUnsavedChanges {...props}>
      <SimpleForm redirect={false}>
        <TextInput source="id" disabled />
        <TextInput source="name" />
        <BooleanInput source="is_async" />
        <CodeInput source="code" />
      </SimpleForm>
    </Edit>
  )
}
