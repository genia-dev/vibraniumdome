"use client"

import * as React from "react";

import { Slider } from "~/app/components/ui/slider";
import { Label } from "~/app/components/ui/label";

import { useAtom } from 'jotai'
import { lowRiskThresholdAtom } from "~/app/state"

//@ts-ignore
export function LowRiskThreshold({ state }) {
  const [lowRiskThreshold, setLowRiskThreshold] = useAtom(lowRiskThresholdAtom)
  const value = lowRiskThreshold ? lowRiskThreshold : state??0.4

  const setValueChange = async (value: number[]) => {
    setLowRiskThreshold(value[0])
  }

  return (
    <>
      <Label htmlFor="low-risk-threshold">
        Low risk threshold: {value}
      </Label>
      <Slider
        id="low-risk-threshold"
        onValueChange={setValueChange}
        value={[value]}
        className="w-[60%]"
        defaultValue={[value]}
        max={1}
        step={0.1}
      />
    </>
  );
}
