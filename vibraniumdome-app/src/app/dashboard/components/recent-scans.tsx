import { format } from "date-fns";
import { api } from "~/trpc/server";

export async function RecentScans() {
  // const scans = [];

  return (
    <div className="space-y-8">
      {/* {scans.map((scan, index) => (
        <div key={index} className="flex items-center">
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">{scan.llmApp.name}</p>
            <p className="text-sm text-muted-foreground">Scan time: {scan.scanTimeMS}ms</p>
          </div>
          <div className="ml-auto font-medium">{format(scan.createdAt, "PP")}</div>
        </div>
      ))} */}
    </div>
  )
}
