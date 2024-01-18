"use client"

import * as React from "react";

import { Label } from "~/app/components/ui/label";
import { Slider } from "~/app/components/ui/slider";

import { useAtom } from 'jotai'
import { highRiskThresholdAtom } from "~/app/state"

//@ts-ignore
export function HighRiskThreshold({ state }) {
  const [highRiskThreshold, setHighRiskThreshold] = useAtom(highRiskThresholdAtom, state)

  const setValueChange = async (value: number[]) => {
    setHighRiskThreshold(value[0] || 0.8)
  }
  
  return (
    <>
      <Label htmlFor="high-risk-threshold">
        High risk threshold: {highRiskThreshold}
      </Label>
      <Slider
        id="high-risk-threshold"
        onValueChange={setValueChange}
        className="w-[60%]"
        defaultValue={[highRiskThreshold]}
        max={1}
        step={0.1}
      />
    </>
  );
}
