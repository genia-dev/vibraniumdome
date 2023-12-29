import * as React from "react";

import { Slider } from "~/app/components/ui/slider";
import { Label } from "~/app/components/ui/label";

export type StateProps = {
  setState: any;
  defaultValue: any;
};

export function HighRiskThreshold({ setState, defaultValue }: StateProps) {
  return (
    <>
      <Label htmlFor="high-risk-threshold">
        High risk threshold
      </Label>
      <Slider
        id="high-risk-threshold"
        onValueChange={setState}
        className="w-[180px]"
        defaultValue={[0.8]}
        max={1}
        step={0.1}
      />
    </>
  );
}
