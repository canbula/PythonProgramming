import {
  Album,
  Atom,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronUp,
  Clock,
  ListTree,
  Search,
} from "lucide-react";
import React from "react";

export const SubHeader = () => {
  return (
    <div className="w-full h-8 bg-[#F0F0F0] flex items-center pl-2 gap-3">
      <ListTree size={20} />
      <Album size={20} />
      <Clock size={20} />
      <Atom size={20} />
      <div className="w-[2px] h-6 bg-slate-400 ml-1"></div>
      <div className="px-2 py-[2px] bg-white">
        <ChevronLeft size={20} />
      </div>
      <div className="px-2 py-[2px] bg-white">
        <ChevronRight size={20} />
      </div>
      <div className="flex flex-1 bg-white justify-between text-slate-300">
        <input disabled />
        <ChevronDown />
      </div>
      <div className="px-2 py-[2px] bg-white">
        <ChevronUp size={20} />
      </div>
      <div className=" bg-white flex justify-between text-slate-300 mr-5">
        <input placeholder="Search..." className="text-sm" />
        <Search color="blue" />
      </div>
    </div>
  );
};
