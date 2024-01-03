"use client"

import { useAtom } from 'jotai'

import { Input } from "~/app/components/ui/input";
import { llmAppAtom } from "~/app/state"


//@ts-ignore
export function LLMAppInput({ state }) {
 const [llmApp, setLlmApp] = useAtom(llmAppAtom)
 var value = llmApp !== '' ? llmApp: state
 setLlmApp(value)

 return (<>
        <Input
          className="w-[180px]"
          id="name"
          value={value}
          onChange={(e) => setLlmApp(e.target.value)}
        />
        </>)
}