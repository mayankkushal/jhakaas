import * as React from "react";
import {
  ArrayField,
  BooleanField,
  ChipField,
  Datagrid,
  List,
  SingleFieldList,
  TextField,
} from "react-admin";

export const CollectionList = (props: any) => (
  <List {...props}>
    <Datagrid rowClick="edit">
      <TextField source="name" />
      <TextField source="id" />
      <BooleanField source="is_strict" />
      <ArrayField source="fields">
        <SingleFieldList>
          <ChipField source="name" />
        </SingleFieldList>
      </ArrayField>
    </Datagrid>
  </List>
);
