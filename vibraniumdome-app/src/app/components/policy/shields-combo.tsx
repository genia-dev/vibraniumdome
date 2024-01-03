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

import { useAtom } from 'jotai'
import { lastShieldAtom, lastShieldMetadataAtom } from "~/app/state"


//@ts-ignore
export function ShieldsCombobox({ shields, policyMetadata }) {
  const [open, setOpen] = React.useState(false)
  const [lastShield, setLastShieldAtom] = useAtom(lastShieldAtom)
  const [lastShieldMetadata, setLastShieldMetadataAtom] = useAtom(lastShieldMetadataAtom)
  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[500px] justify-between"
        >
          {lastShield
          //@ts-ignore
            ? shields.find((shield) => shield.value.toLowerCase() === lastShield)?.value
            : "Select shield..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[500px] p-0">
        <Command>
          <CommandInput placeholder="Search shield..." />
          <CommandEmpty>No shield found.</CommandEmpty>
          <CommandGroup>
            {
              //@ts-ignore
              shields.map((shield) => (
              <CommandItem
                key={shield.key}
                value={shield.value}
                onSelect={(currentValue) => {
                  const shieldMetadata = policyMetadata.find((shield) => shield.full_name.toLowerCase() === currentValue)
                  setLastShieldMetadataAtom(JSON.stringify(shieldMetadata.metadata))
                  setLastShieldAtom(currentValue)
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
