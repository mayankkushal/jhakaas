import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import { makeStyles } from '@material-ui/core/styles'
// @ts-ignore
import { JsonEditor as Editor } from 'jsoneditor-react'
import 'jsoneditor-react/es/editor.min.css'
import React, { useEffect, useState } from 'react'
import {
  Button,
  Loading,
  Title,
  Toolbar,
  useCreate,
  useQuery,
} from 'react-admin'
import { useParams } from 'react-router'
import { useToolbarStyles } from '../../../styles/toolbar'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  cards: {
    padding: theme.spacing(2),
    height: '95%',
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
  },
  space: {
    marginTop: theme.spacing(1),
  },
}))

const DataEditToolbar = (props: any) => {
  const classes = useToolbarStyles(props)
  return (
    <Toolbar {...props}>
      <div className={classes.defaultToolbar}>
        <Button
          onSuccess={() => {}}
          submitOnEnter={false}
          redirect={() => {}}
          onClick={props.handleSave}
          {...props}
          label="Save"
        />
      </div>
    </Toolbar>
  )
}

const DataCreateView = (props: any) => {
  const [jsonData, setJsonData] = useState()
  const classes = useStyles()
  const params: { id: string; data_id: string } = useParams()
  const query = useQuery({
    type: 'getOne',
    resource: `collection`,
    payload: { id: params.id },
  })

  const [save] = useCreate(`collection/${params.id}/data`, jsonData)

  const handleSave = () => {
    save()
  }

  useEffect(() => {
    if (query.data) {
      let initMap: any = {}
      query.data.fields.forEach(
        (field: { name: string }) => (initMap[field.name] = '')
      )
      setJsonData(initMap)
    }
  }, [query])

  if (query.loading) return <Loading />
  if (!query.data) return null

  return (
    <Card className={classes.cards}>
      <Title title="Data add" />
      <CardContent>
        {query.data && jsonData && (
          <Editor value={jsonData} onChange={setJsonData} />
        )}
        <DataEditToolbar record={query.data} handleSave={handleSave} />
      </CardContent>
    </Card>
  )
}

export default DataCreateView
