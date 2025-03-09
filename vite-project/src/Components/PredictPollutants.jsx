import React, { useState } from 'react';
import Sidebar from './Sidebar';
import { FaUpload, FaDownload } from 'react-icons/fa'; // Import icons from react-icons


function PredictPollutants() {
  const [file, setFile] = useState(null); // State to store the selected file
  const [downloadUrl, setDownloadUrl] = useState(null); // State to store the download URL
  const [isUploading, setIsUploading] = useState(false); // State to handle loading during upload

  // Handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file upload
  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a CSV file first!");
      return;
    }

    setIsUploading(true); // Start loading

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Send the file to the backend
      const response = await fetch('http://localhost:8000/upload_csv/', {
        method: 'POST',
        body: formData,
      });
      console.log(response.blob)

      if (response.ok) {
        // Convert the response to a Blob
        const blob = await response.blob();

        const text = await blob.text();
        console.log("CSV Content:", text);  

        // Create a download URL for the Blob
        const url = window.URL.createObjectURL(blob);
        setDownloadUrl(url); // Set the download URL

        alert('CSV file sent to backend!')
      } else {
        alert('Error sending file');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while uploading the file.');
    } finally {
      setIsUploading(false); // Stop loading
    }
  };

  // Handle file download
  const handleDownload = () => {
    if (!downloadUrl) {
      alert("No predictions available to download. Please upload a CSV file first.");
      return;
    }

    // Create a temporary <a> element to trigger the download
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = 'predictions.csv'; // Name of the downloaded file
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
       <div className="flex min-h-screen">
      {/* Sidebar Inside the Dashboard */}
      <Sidebar />
      <div className="container mx-auto p-6 bg-gradient-to-r from-blue-300 via-purple-200 to-pink-300 bg-opacity-50 relative h-screen w-full flex justify-center items-center">
        <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md w-full">
          <h1 className="text-2xl font-semibold mb-6 text-gray-800">Upload CSV File</h1>

          {/* File Input */}
          <div className="mb-6">
            <label className="block mb-2 text-sm font-medium text-gray-700">
              Choose a CSV file
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>

          {/* Upload Button */}
          <button
            onClick={handleSubmit}
            disabled={isUploading}
            className="w-full flex items-center justify-center bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300 transition duration-300 mb-4"
          >
            <FaUpload className="mr-2" />
            {isUploading ? 'Uploading...' : 'Upload CSV'}
          </button>

          {/* Download Button */}
          <button
            onClick={handleDownload}
            disabled={!downloadUrl}
            className="w-full flex items-center justify-center bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:bg-green-300 transition duration-300"
          >
            <FaDownload className="mr-2" />
            Download Predictions
          </button>

          {/* Message */}
          <p className="mt-4 text-sm text-gray-600">
            Collect your predictions data here.
          </p>
        </div>
      </div>
    </div>
  );
}
export default PredictPollutants;
