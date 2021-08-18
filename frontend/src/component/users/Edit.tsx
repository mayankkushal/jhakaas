import * as React from "react";
import {
  BooleanInput,
  Edit,
  SimpleForm,
  TextInput,
  useEditController,
} from "react-admin";

export const UserEdit = (props: any) => {
  const { record } = useEditController(props);
  return (
    <Edit {...props} title={`Edit ${record?.email}`}>
      <SimpleForm>
        <TextInput source="email" />
        <BooleanInput source="is_active" />
        <BooleanInput source="is_superuser" />
        <BooleanInput source="is_verified" />
        <TextInput source="firstName" />
        <TextInput source="lastName" />
      </SimpleForm>
    </Edit>
  );
};
