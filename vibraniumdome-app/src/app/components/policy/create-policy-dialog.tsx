"use client";

import * as React from "react";
import { Button } from "~/app/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/app/components/ui/dialog";
import { Label } from "~/app/components/ui/label";
import { ShieldsCombobox } from "~/app/components/policy/shields-combo";
import { Info } from "lucide-react";
import { useAtom } from 'jotai'
import { inputShieldsAtom, outputShieldsAtom, lastShieldAtom } from "~/app/state"
import { v4 as uuidv4 } from 'uuid';

export type Policy = {
  id: string;
  name: string;
  llmAppName: number;
  content: string;
  createdAt: string;
};

export type Props = {
  isinput: boolean;
  title: string;
  shields: { key: string; value: string }[];
  policyMetadata: { type: string; full_name: string }[];
};

export function CreateShieldDialog({
  isinput,
  title,
  shields,
  policyMetadata,
}: Props) {
  const [open, setOpen] = React.useState(false);
  const [inputShields, setInputShieldsAtom] = useAtom(inputShieldsAtom)
  const [outputShields, setOutputShieldsAtom] = useAtom(outputShieldsAtom)
  const [lastShield, setLastShieldAtom] = useAtom(lastShieldAtom)


  const saveChanges = () => {
    setOpen(false);
    const shield = policyMetadata.find((shield) => shield.full_name.toLowerCase() === lastShield)
    if (isinput) {
      //@ts-ignore
      setInputShieldsAtom([...inputShields, {id: uuidv4(), shield: shield?.full_name}])
    } else {
      //@ts-ignore
      setOutputShieldsAtom([...outputShields, {id: uuidv4(), shield: shield?.full_name}])
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>{title}</Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-[825px]">
        <DialogHeader>
          <DialogTitle>Add shield</DialogTitle>
          <DialogDescription>
            Select a shield and update its configuration
            <a target="blank" href="https://docs.vibraniumdome.com/shields/introduction"><Info height={16} className="inline"/></a>
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4"></div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="llmAppName" className="text-right">
              Shield
            </Label>
            <ShieldsCombobox
              shields={shields}
            />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={saveChanges}>
            Add
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
