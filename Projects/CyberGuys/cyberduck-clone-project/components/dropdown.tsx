"use client";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import {
  DatabaseBackupIcon,
  DatabaseBackup,
  DatabaseZap,
  Cloud,
  Database,
  FilePlus,
  CloudDrizzle,
  ChevronDown,
} from "lucide-react";
import { useState } from "react";

const services = [
  { id: 1, icon: DatabaseBackupIcon, label: "FTP-SSL (Explicit AUTH TLS)" },
  { id: 2, icon: DatabaseBackupIcon, label: "FTP (File Transfer Protocol)" },
  { id: 3, icon: DatabaseBackupIcon, label: "FTP-SSL (Explicit AUTH TLS)" },
  { id: 4, icon: DatabaseBackup, label: "SFTP (SSH File Transfer Protocol)" },
  { id: 5, icon: Cloud, label: "WebDAV (HTTP)" },
  { id: 6, icon: CloudDrizzle, label: "WebDAV (HTTPS)" },
  { id: 7, icon: Database, label: "SMB (Server Message Block)" },
  { id: 8, icon: DatabaseZap, label: "Amazon S3" },
  { id: 9, icon: Cloud, label: "Google Cloud Storage" },

  { id: 10, icon: FilePlus, label: "More Options..." },
];

const Dropdown = () => {
  const [selected, setSelected] = useState(1);
  const [open, setOpen] = useState(false);

  const handleSelect = (id: number) => {
    setSelected(id);
    setOpen(false); // Menü tıklanınca kapanmasını sağlamak için open state'ini false yapıyoruz.
  };

  let selectedItem = services.find((item) => item.id === selected)!;

  return (
    <div className="w-full p-1 bg-white border-2 border-slate-300">
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger
          onClick={() => setOpen(!open)}
          className="flex justify-between w-full"
        >
          <div className="flex gap-2">
            {<selectedItem.icon className="size-4" />}
            {selectedItem.label}
          </div>
          <span>
            <ChevronDown />
          </span>
        </DropdownMenuTrigger>
        <DropdownMenuContent className=" w-[29rem]">
          <DropdownMenuGroup>
            {services.map((service) => (
              <div
                key={service.id}
                className="flex hover:bg-slate-100 cursor-pointer"
                onClick={() => handleSelect(service.id)}
              >
                <DropdownMenuItem>
                  {<service.icon className="size-4" />}
                </DropdownMenuItem>
                <DropdownMenuLabel>{service.label}</DropdownMenuLabel>
              </div>
            ))}
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default Dropdown;
