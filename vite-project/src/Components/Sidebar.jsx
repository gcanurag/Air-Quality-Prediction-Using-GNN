import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AiOutlineClose } from 'react-icons/ai'; // Importing the close icon

const Sidebar = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true); // State to toggle the sidebar visibility

  // Toggle the sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div
      className={`w-64 bg-gray-800 text-white p-4 transition-all duration-300 ease-in-out ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
    >
      {/* Close Button */}
      <button
        onClick={toggleSidebar}
        className="absolute top-4 right-4 text-white text-2xl"
      >
        <AiOutlineClose />
      </button>

      <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>
      <ul>
        <li className="mb-4 hover:bg-gray-700 p-2 rounded">
          <Link to="/">Home</Link>
        </li>
        <li className="mb-4 hover:bg-gray-700 p-2 rounded">
          <Link to="/predict">Predict Pollutants</Link>
        </li>
        <li className="mb-4 hover:bg-gray-700 p-2 rounded">
          <a href="#">Data Analysis</a>
        </li>
        <li className="mb-4 hover:bg-gray-700 p-2 rounded">
          <a href="#">Reports</a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
