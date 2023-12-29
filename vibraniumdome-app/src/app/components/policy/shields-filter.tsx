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

export function ShieldsFilter({setState, defaultValue}: StateProps) {
  return (
    <Select onValueChange={setState} value={defaultValue}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select Shields Filter" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Shields Filter</SelectLabel>
          <SelectItem value="all">All</SelectItem>
          <SelectItem value="dry-run">Dry-Run</SelectItem>
          <SelectItem value="skip">Skip</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
