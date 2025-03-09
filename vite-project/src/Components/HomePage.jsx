import { useState } from "react";
import { FaSearch, FaCloud, FaSmog, FaWind } from "react-icons/fa";
import Sidebar from "./Sidebar";

const Homepage = () => {
  const [location, setLocation] = useState("");
  const [aqi, setAqi] = useState("--");

  const handleSearch = () => {
    const fakeAqi = Math.floor(Math.random() * 300);
    setAqi(fakeAqi);
  };

  return (
    <div className="flex min-h-screen">
    {/* Sidebar Inside the Dashboard */}
    <Sidebar />
    <div className="min-h-screen w-full  bg-gradient-to-r from-blue-300 via-purple-200 to-pink-300 bg-opacity-50 relative flex flex-col items-center text-gray-800 p-6 ">
      <h1 className="text-4xl font-bold text-blue-600 mb-4">Air Quality Analysis & Prediction</h1>
      <p className="text-lg text-gray-600 mb-6">Get the fine-grained analysis of air pollutants concentration in your city</p>

      <div className="flex items-center bg-white shadow-lg rounded-lg overflow-hidden w-80">
        <input
          type="text"
          placeholder="Enter location..."
          className="px-4 py-2 w-full outline-none"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <button onClick={handleSearch} className="bg-blue-500 text-white px-4 py-2">
          <FaSearch />
        </button>
      </div>

      <div className="mt-8 bg-white shadow-md p-6 rounded-lg w-80 text-center">
        <h2 className="text-2xl font-semibold">Current AQI</h2>
        <p className={`text-3xl font-bold mt-2 ${aqi < 50 ? "text-green-500" : aqi < 150 ? "text-yellow-500" : "text-red-500"}`}>
          {aqi}
        </p>
        <p className="text-sm text-gray-600 mt-2">
          {aqi < 50 ? "Good Air Quality 🌿" : aqi < 150 ? "Moderate 🌥️" : "Unhealthy ⚠️"}
        </p>
      </div>

      <div className="mt-8 flex gap-4">
        <div className="bg-white p-4 shadow-md rounded-lg text-center">
          <FaCloud className="text-blue-400 text-4xl mx-auto" />
          <p className="mt-2 text-gray-600">Humidity</p>
        </div>
        <div className="bg-white p-4 shadow-md rounded-lg text-center">
          <FaSmog className="text-gray-500 text-4xl mx-auto" />
          <p className="mt-2 text-gray-600">PM 2.5</p>
        </div>
        <div className="bg-white p-4 shadow-md rounded-lg text-center">
          <FaWind className="text-blue-300 text-4xl mx-auto" />
          <p className="mt-2 text-gray-600">Wind Speed</p>
        </div>
      </div>
    </div>
    </div>
  );
};

export default Homepage;
