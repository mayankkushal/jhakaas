import { Modal, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import keyBy from "lodash/keyBy";
import React, { useState } from "react";
import {
  BooleanField,
  BooleanInput,
  Button,
  Create,
  CreateButton,
  Datagrid,
  DeleteButton,
  Edit,
  ListContextProvider,
  required,
  SaveButton,
  SelectInput,
  SimpleForm,
  TextField,
  TextInput,
  Toolbar,
  useEditController,
  useQuery,
  useRefresh,
} from "react-admin";
import { Route, useHistory } from "react-router-dom";

const useStyles = makeStyles(
  (theme) => ({
    toolbar: {
      backgroundColor:
        theme.palette.type === "light"
          ? theme.palette.grey[100]
          : theme.palette.grey[900],
    },
    desktopToolbar: {
      marginTop: theme.spacing(2),
    },
    mobileToolbar: {
      position: "fixed",
      bottom: 0,
      left: 0,
      right: 0,
      padding: "16px",
      width: "100%",
      boxSizing: "border-box",
      flexShrink: 0,
      zIndex: 2,
    },
    modal: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    paper: {
      backgroundColor: theme.palette.background.paper,
      border: "2px solid #000",
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
    },
    defaultToolbar: {
      flex: 1,
      display: "flex",
      justifyContent: "space-between",
    },
    spacer: {
      [theme.breakpoints.down("xs")]: {
        height: "5em",
      },
    },
  }),
  { name: "RaToolbar" }
);

const Aside = ({ record }: { record?: any }) => {
  const [page, setPage] = useState(1);
  const perPage = 50;
  const query = useQuery({
    type: "getList",
    resource: `collection/${record?.id}/fields`,
    payload: {
      pagination: { page, perPage },
      sort: { field: "createdAt", order: "DESC" },
    },
  });
  return (
    <div style={{ width: "30vw", margin: "1em" }}>
      <Typography variant="h6">Fields</Typography>
      <ListContextProvider
        value={{
          ...query,
          data: keyBy(query.data, "id"),
          ids: query.data?.map(({ id }: { id: any }) => id),
          page,
          perPage,
          setPage,
          resource: "field",
          currentSort: { field: "id", order: "ASC" },
          selectedIds: [],
        }}
      >
        <Datagrid rowClick="edit" resource={`collection/${record?.id}/field`}>
          <TextField source="name" />
          <TextField source="type" />
          <BooleanField source="indexed" />
          <DeleteButton
            mutationMode={"pessimistic"}
            confirmTitle={"This change is irreversible"}
          />
        </Datagrid>
      </ListContextProvider>
    </div>
  );
};

const CollectionEditToolbar = (props: any) => {
  const classes = useStyles(props);
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
  );
};

const FieldCreateToolbar = (props: any) => {
  const classes = useStyles(props);
  const history = useHistory();
  const refresh = useRefresh();

  const push = () => {
    history.push(`/collection/${props.collection?.id}`);
  };
  const onSuccess = () => {
    push();
    refresh();
  };
  return (
    <Toolbar {...props}>
      <div className={classes.defaultToolbar}>
        <SaveButton
          disabled={props.pristine}
          {...props}
          onSuccess={onSuccess}
        />

        <Button label="Cancel" onClick={push} />
      </div>
    </Toolbar>
  );
};

const FieldCreate = (props: any) => {
  return (
    <Create
      {...props}
      resource={`collection/${props.collection?.id}/field/add`}
    >
      <SimpleForm
        toolbar={<FieldCreateToolbar collection={props.collection} />}
      >
        <TextInput source="name" validate={required()} />
        <SelectInput
          source="type"
          choices={[
            { id: "string", name: "String" },
            { id: "bool", name: "Boolean" },
            { id: "null", name: "Null" },
          ]}
          validate={required()}
        />
        <BooleanInput source="indexed" />
      </SimpleForm>
    </Create>
  );
};

export const CollectionEdit = (props: any) => {
  const { record } = useEditController(props);
  const classes = useStyles();
  return (
    <div>
      <Edit {...props} aside={record && <Aside />} title={record?.name}>
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
  );
};
