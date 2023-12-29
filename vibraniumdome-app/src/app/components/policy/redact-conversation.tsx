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
    <Select onValueChange={setState} value={defaultValue}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Redact Conversation" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Redact Conversation</SelectLabel>
          <SelectItem value="yes">Yes</SelectItem>
          <SelectItem value="no">No</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
