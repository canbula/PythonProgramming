import React from "react";
import Dropdown from "./dropdown";
import ConnectionModal from "./connection-modal";
import Separator from "./seperator";
import { Input } from "./ui/input";
import {
  ChevronDown,
  FolderUp,
  GalleryVerticalEnd,
  Info,
  Pencil,
  RotateCcw,
  Settings,
  SquareArrowUp,
} from "lucide-react";

const Header = () => {
  return (
    <div className="flex justify-between w-full h-20 bg-[#F0F0F0]">
      <div className="flex items-center">
        <ConnectionModal />
        <Separator />
        <section className="ml-2 flex items-center">
          <div className="flex border-2 border-slate-500 rounded-md h-8">
            <Input className="h-7  " defaultValue={"Quick Connect"} />
            <ChevronDown className="w-5" />
          </div>
          <div className="ml-2 flex flex-col items-center justify-center hover:bg-blue-300/30 transition-all cursor-pointer h-20  ">
            <Settings size={38} />
            <p>Action</p>
          </div>
        </section>
        <Separator />
        <section className="ml-2 flex items-center">
          <div className="flex flex-col items-center text-slate-400">
            <Info size={30} />
            <p>Get info</p>
          </div>
          <div className="flex flex-col items-center text-slate-400 ml-2 mr-2">
            <RotateCcw size={30} />
            <p>Refresh</p>
          </div>
        </section>
        <Separator />
        <section className="ml-2 flex items-center">
          <div className="flex flex-col items-center text-slate-400 ml-3 mr-3">
            <Pencil size={30} />
            <p>Edit</p>
          </div>
        </section>
        <Separator />
        <section className="ml-2 flex items-center">
          <div className="flex flex-col items-center text-slate-400">
            <FolderUp size={30} />
            <p>Upload</p>
          </div>
          <div className="flex flex-col items-center text-slate-400 ml-2 mr-2">
            <GalleryVerticalEnd size={30} />
            <p>Transfers</p>
          </div>
        </section>
      </div>
      <div className="flex flex-col items-center text-slate-400 ml-2 mr-2 justify-center">
        <SquareArrowUp size={30} />
        <p>Disconnect</p>
      </div>
    </div>
  );
};

export default Header;
