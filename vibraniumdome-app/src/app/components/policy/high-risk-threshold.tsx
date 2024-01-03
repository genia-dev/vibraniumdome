"use client"

import * as React from "react";

import { Label } from "~/app/components/ui/label";
import { Slider } from "~/app/components/ui/slider";

import { useAtom } from 'jotai'
import { highRiskThresholdAtom } from "~/app/state"

//@ts-ignore
export function HighRiskThreshold({ state }) {
  const [highRiskThreshold, setHighRiskThreshold] = useAtom(highRiskThresholdAtom)
  const value = highRiskThreshold ? highRiskThreshold : state??0.8

  const setValueChange = async (value: number[]) => {
    setHighRiskThreshold(value[0])
  }
  
  return (
    <>
      <Label htmlFor="high-risk-threshold">
        High risk threshold: {value}
      </Label>
      <Slider
        id="high-risk-threshold"
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
