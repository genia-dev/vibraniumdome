"use client"

import * as React from "react";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "~/app/components/ui/select";

import { useAtom } from 'jotai'
import { shieldsFilterAtom } from "~/app/state"

//@ts-ignore
export function ShieldsFilter({ state }) {
  const [shieldsFilter, setShieldsFilter] = useAtom(shieldsFilterAtom)
  return (
    <Select name="shields-filter"
            onValueChange={setShieldsFilter}
            value={shieldsFilter || state}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="select..." />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Shields execution mode:</SelectLabel>
          <SelectItem value="all">All</SelectItem>
          <SelectItem value="dry-run">Dry-Run</SelectItem>
          <SelectItem value="skip">Skip</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}
