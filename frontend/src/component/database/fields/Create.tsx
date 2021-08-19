import React from "react";
import {
  BooleanInput,
  Button,
  Create,
  required,
  SaveButton,
  SelectInput,
  SimpleForm,
  TextInput,
  Toolbar,
  useRefresh,
} from "react-admin";
import { useHistory } from "react-router";
import { useToolbarStyles } from "../../../styles/toolbar";

const FieldCreateToolbar = (props: any) => {
  const classes = useToolbarStyles(props);
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

export const FieldCreate = (props: any) => {
  console.log("props", props);
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
