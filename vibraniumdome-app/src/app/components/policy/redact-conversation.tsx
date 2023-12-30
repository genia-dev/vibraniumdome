import * as React from "react"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "~/app/components/ui/select"

export type StateProps = {
  setState: any
  defaultValue: any
};

export function RedactConversation({setState, defaultValue}: StateProps) {
  return (
    <Select name="redact-conversation" onValueChange={setState} value={defaultValue}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="select..." />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Redact conversation sensetive content?</SelectLabel>
          <SelectItem value="yes">Yes</SelectItem>
          <SelectItem value="no">No</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
