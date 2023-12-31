import * as React from "react";

import { Slider } from "~/app/components/ui/slider";
import { Label } from "~/app/components/ui/label";

export type StateProps = {
  setState: any;
  defaultValue: any;
};

export function LowRiskThreshold({ setState, defaultValue}: StateProps) {
  return (
    <>
      <Label htmlFor="low-risk-threshold">
        Low risk threshold: {defaultValue??0.4}
      </Label>
      <Slider
        id="low-risk-threshold"
        onValueChange={setState}
        value={[defaultValue??0.4]}
        className="w-[60%]"
        defaultValue={[0.4]}
        max={1}
        step={0.1}
      />
    </>
  );
}
