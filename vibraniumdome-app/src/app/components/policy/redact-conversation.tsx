"use client"

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

import { useAtom } from 'jotai'
import { redactConversationAtom } from "~/app/state"

//@ts-ignore
export function RedactConversation({ state }) {
  const [redactConversation, setRedactConversation] = useAtom(redactConversationAtom)

  return (
    <Select name="redact-conversation" 
            onValueChange={setRedactConversation}
            value={redactConversation || state === true ? "yes" : "no"}>
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
