import * as React from 'react'
import AceEditor from 'react-ace'
import { useInput} from 'react-admin'

import 'ace-builds/src-noconflict/mode-python'
import "ace-builds/src-noconflict/theme-monokai"

export const CodeField = (props: any) => {
  const {
    input: { onChange, value}
  } = useInput(props);

  return (
    <AceEditor
      mode="python"
      theme="monokai"
      width="100%"
      onChange={onChange}
      value={value}
      name="UNIQUE_ID_OF_DIV"
      editorProps={{ $blockScrolling: true }}
    />
  )
}


export const CodeInput = (props: any) => {
  const {source, ...rest} = props;
  return <CodeField source={source} {...rest} />
}