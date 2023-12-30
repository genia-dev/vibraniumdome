import * as React from "react";

import { Label } from "~/app/components/ui/label";
import { Slider } from "~/app/components/ui/slider";

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
        className="w-[60%]"
        defaultValue={[0.8]}
        max={1}
        step={0.1}
      />
    </>
  );
}
