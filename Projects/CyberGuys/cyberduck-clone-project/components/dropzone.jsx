import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";

const Dropzone = ({ onDrop }) => {
  const handleDrop = useCallback(
    (acceptedFiles) => {
      onDrop(acceptedFiles);
    },
    [onDrop]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleDrop,
  });

  return (
    <div
      {...getRootProps()}
      className="border-2 border-dashed border-gray-400 rounded-md p-5 text-center cursor-pointer w-full max-w-lg mx-auto"
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>Drop the files here...</p>
      ) : (
        <p>Drag 'n' drop some files here, or click to select files</p>
      )}
    </div>
  );
};

export default Dropzone;
