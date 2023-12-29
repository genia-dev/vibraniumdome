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

export function HighRiskThreshold({setState, defaultValue}: StateProps) {
  return (
    <Select onValueChange={setState} value={defaultValue}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="High Risk Threshold" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>High Risk Threshold</SelectLabel>
          <SelectItem value="0.0">0.0</SelectItem>
          <SelectItem value="0.1">0.1</SelectItem>
          <SelectItem value="0.2">0.2</SelectItem>
          <SelectItem value="0.3">0.3</SelectItem>
          <SelectItem value="0.4">0.4</SelectItem>
          <SelectItem value="0.5">0.5</SelectItem>
          <SelectItem value="0.6">0.6</SelectItem>
          <SelectItem value="0.7">0.7</SelectItem>
          <SelectItem value="0.8">0.8</SelectItem>
          <SelectItem value="0.9">0.9</SelectItem>
          <SelectItem value="1.0">1.0</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
