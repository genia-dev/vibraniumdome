"use client";

import * as React from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { ArrowUpDown, MoreHorizontal } from "lucide-react";

import { Button } from "~/app/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "~/app/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/app/components/ui/table";

import { useAtom, useSetAtom } from 'jotai'
import { inputShieldsAtom, outputShieldsAtom, lastShieldAtom, lastShieldMetadataAtom } from "~/app/state"

import { useRouter } from "next/navigation";

export type Shield = {
  id: string;
  shield: string;
};


//@ts-ignore
export const createColumns = (shieldCategory: string, policyId: string): ColumnDef<Shield>[] => {
  const router = useRouter();

  const [inputShields, setInputShieldsAtom] = useAtom(inputShieldsAtom)
  const [outputShields, setOutputShieldsAtom] = useAtom(outputShieldsAtom)
  const setLastShield = useSetAtom(lastShieldAtom)
  const setLastShieldMetadata = useSetAtom(lastShieldMetadataAtom)

  return [{
    id: "select",
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "shield",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Shield
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
    cell: ({ row }) => (
      <div className="lowercase">{row.getValue("shield")}</div>
    ),
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const shield = row.original;

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => {
                setLastShield(shield.shield)
                setLastShieldMetadata(JSON.stringify(shield.metadata));
                
                router.push(policyId ? `/shield/edit?category=${shieldCategory}&policyId=${policyId}` : `/shield/edit?category=${shieldCategory}`);
                router.refresh();
              }}
            >
              Edit Shield
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={() => {
                setLastShield(shield.shield)
                setLastShieldMetadata(JSON.stringify(shield.metadata));
                
                router.push(policyId ? `/shield/view?category=${shieldCategory}&policyId=${policyId}` : `/shield/view?category=${shieldCategory}`);
                router.refresh();
              }}
            >
              View Shield
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={() => {
                if (shieldCategory=="input") {
                  //@ts-ignore
                  setInputShieldsAtom(inputShields.filter(item => item.shield !== shield.shield));
                } else {
                  //@ts-ignore
                  setOutputShieldsAtom(outputShields.filter(item => item.shield !== shield.shield));
                }
              }}
            >
              Delete Shield
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
]};

//@ts-ignore
export function ShieldsDataTable({ data, shieldCategory, policyId }) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    [],
  );
  
  const [inputShields, setInputShieldsAtom] = useAtom(inputShieldsAtom)
  const [outputShields, setOutputShieldsAtom] = useAtom(outputShieldsAtom)

  if (shieldCategory=="input") {
    data = inputShields.length === 0 ? data : inputShields
    setInputShieldsAtom(data)
  } else {
    data = outputShields.length === 0 ? data : outputShields
    setOutputShieldsAtom(data)
  }

  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});

  const table = useReactTable({
    data,
    //@ts-ignore
    columns: createColumns(shieldCategory, policyId),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  return (
    <div className="w-full">
      <div className="flex"></div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={createColumns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
