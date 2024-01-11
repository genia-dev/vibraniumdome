"use client"

import { useAtom } from 'jotai'

import { Textarea } from "~/app/components/ui/textarea"
import { lastShieldMetadataAtom } from "~/app/state"

//@ts-ignore
export function ShieldMetadata() {
  const [lastShieldMetadata, setLastShieldMetadata] = useAtom(lastShieldMetadataAtom)
  const setValueChange = async (e) => {
    setLastShieldMetadata(e.target.value)
  }

  return (
        <Textarea className="col-span-3" 
          value={ lastShieldMetadata }
          onChange={setValueChange}
          placeholder="" />
        )
}