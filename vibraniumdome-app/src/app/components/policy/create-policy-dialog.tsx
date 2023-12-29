"use client"

import * as React from "react"
import { Button } from "~/app/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/app/components/ui/dialog"
import { Label } from "~/app/components/ui/label"
import { ShieldsCombobox } from "~/app/components/policy/shields-combo"

import { useDispatch } from 'react-redux';
import { addInputShield, addOutputShield } from '~/app/store/actions';


export type Policy = {
    id: string
    name: string
    llmAppName: number
    content: string
    createdAt: string
}

export type CreateShieldDialogProps = {
    isinput: boolean;
    title: string;
    shields: { key: string; value: string }[];
};

export function CreateShieldDialog({ isinput, title, shields }: CreateShieldDialogProps) {
    const [open, setOpen] = React.useState(false);
    const [value, setValue] = React.useState("")
    const dispatch = useDispatch();
    
    const saveChanges = () => {
        setOpen(false);
        if (isinput) {
            dispatch(addInputShield(value))
        } else {
            dispatch(addOutputShield(value))
        }
      };

    return (
    <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
            <Button>{title}</Button>
        </DialogTrigger>
        
        <DialogContent className="sm:max-w-[825px]">
            <DialogHeader>
            <DialogTitle>Create shield</DialogTitle>
            <DialogDescription>
                Select shield. Click save when you're done.
            </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="llmAppName" className="text-right">
                Shield
                </Label>
                <ShieldsCombobox value={value} setValue={setValue} shields={shields}/>
            </div>
            </div>
            <DialogFooter>
                <Button type="submit" onClick={saveChanges}>Save changes</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
    )
}