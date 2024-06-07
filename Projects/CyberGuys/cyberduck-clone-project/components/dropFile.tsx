"use client";

import React, { useState } from "react";
import Dropzone from "../components/Dropzone";

const DropFile = ({ handleDrop, handleUpload, images }) => {
  // const [images, setImages] = useState([]);
  // const [files, setFiles] = useState([]);

  // const handleDrop = (acceptedFiles) => {
  //   const newImages = acceptedFiles.map((file) => URL.createObjectURL(file));
  //   setImages((prev) => [...prev, ...newImages]);
  //   setFiles((prev) => [...prev, ...acceptedFiles]);
  // };

  // const handleUpload = () => {
  //   const formData = new FormData();
  //   files.forEach((file) => formData.append("file", file));

  //   fetch("http://127.0.0.1:5000/upload", {
  //     method: "POST",
  //     body: formData,
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("Success:", data);
  //     })
  //     .catch((error) => {
  //       console.error("Error:", error);
  //     });
  // };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">
        Image Upload with Drag and Drop
      </h1>
      <Dropzone onDrop={handleDrop} />
      <div className="flex flex-wrap justify-center mt-4">
        {images.map((image, index) => (
          <img
            key={index}
            src={image}
            alt={`Uploaded ${index}`}
            className="w-36 h-36 object-cover m-2 rounded-md"
          />
        ))}
      </div>
      <button
        onClick={handleUpload}
        className="mt-4 px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
      >
        Gönder
      </button>
    </div>
  );
};

export default DropFile;
