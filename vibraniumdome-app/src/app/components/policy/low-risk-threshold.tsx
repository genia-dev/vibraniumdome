"use client"

import * as React from "react";

import { Slider } from "~/app/components/ui/slider";
import { Label } from "~/app/components/ui/label";

import { useAtom } from 'jotai'
import { lowRiskThresholdAtom } from "~/app/state"

//@ts-ignore
export function LowRiskThreshold({ state }) {
  const [lowRiskThreshold, setLowRiskThreshold] = useAtom(lowRiskThresholdAtom, state)

  const setValueChange = async (value: number[]) => {
    setLowRiskThreshold(value[0])
  }

  return (
    <>
      <Label htmlFor="low-risk-threshold">
        Low risk threshold: {lowRiskThreshold}
      </Label>
      <Slider
        id="low-risk-threshold"
        onValueChange={setValueChange}
        className="w-[60%]"
        defaultValue={[lowRiskThreshold]}
        max={1}
        step={0.1}
      />
    </>
  );
}
