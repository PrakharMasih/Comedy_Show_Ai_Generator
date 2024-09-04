import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  async function handleClick() {
    try {
        const response = await fetch("http://localhost:9080/delete", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        console.log(data);

        window.dispatchEvent(new Event('clearChats'));
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      }
  }

  return (
    <div className="flex w-full lg:full h-12 lg:h-10 fixed backdrop-blur-sm shadow-lg justify-between items-center">
      <div className="pl-8 font-bold text-indigo-700 italic mt-3 mb-3">AI Comedy Show</div>
      <div className="pr-8 ">
        <button className="px-6 py-3 font-sans text-xs font-bold mt-3 mb-3 text-center text-gray-900 uppercase align-middle transition-all rounded-full select-none disabled:opacity-50 disabled:shadow-none disabled:pointer-events-none hover:bg-gray-900/10 active:bg-gray-900/20"
    type="button" onClick={() => handleClick()}> start New Chat</button>
      </div>
    </div>
  );
};

export default Navbar;
