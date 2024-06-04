import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ArrowBigDownDash } from "lucide-react";
import DropFile from "./dropFile";

const CollapsibleComp = ({ handleDrop, handleUpload, images }) => {
  return (
    <Collapsible>
      <CollapsibleTrigger>
        <div className="flex gap-3">
          <ArrowBigDownDash className="bg-slate-200 rounded-full size-7 p-[2px] hover:bg-slate-100" />
          <p>Send your image here</p>
        </div>
      </CollapsibleTrigger>
      <CollapsibleContent>
        <DropFile
          handleDrop={handleDrop}
          handleUpload={handleUpload}
          images={images}
        />
      </CollapsibleContent>
    </Collapsible>
  );
};

export default CollapsibleComp;
