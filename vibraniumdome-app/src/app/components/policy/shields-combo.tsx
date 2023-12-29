"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { Button } from "~/app/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "~/app/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "~/app/components/ui/popover"

export type Shields = {
 shields: { key: string; value: string }[];
 value: any
 setValue: any
};

//@ts-ignore
export function ShieldsCombobox({ shields, value, setValue }: Shields) {
  const [open, setOpen] = React.useState(false)
  
  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[500px] justify-between"
        >
          {value
            ? shields.find((shield) => shield.value === value)?.value
            : "Select shield..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[500px] p-0">
        <Command>
          <CommandInput placeholder="Search shield..." />
          <CommandEmpty>No shield found.</CommandEmpty>
          <CommandGroup>
            {shields.map((shield) => (
              <CommandItem
                key={shield.key}
                value={shield.value}
                onSelect={(currentValue) => {
                 currentValue
                 setValue(currentValue)
                 setOpen(false)
                }}
              >
                {shield.value}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
