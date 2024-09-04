import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";


const Home = () => {
  const [chats, setChats] = useState([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [videoUrls, setVideoUrls] = useState({});
  const [generatingVideos, setGeneratingVideos] = useState({});
  const navigation = useNavigate();
  const clearChats = useCallback(() => {
    setChats([]);
  }, []);

  useEffect(() => {
    const handleClearChats = () => clearChats();
    window.addEventListener('clearChats', handleClearChats);
    return () => window.removeEventListener('clearChats', handleClearChats);
  }, [clearChats]);

  useEffect(() => {
    getConversations();
  }, []);


  async function getConversations() {
    try {
      const response = await fetch("http://localhost:9080/chat", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      setChats(data);
    } catch (error) {
      console.error("Failed to fetch conversations:", error);
    }
  }

  async function handleSubmit() {
    if (!question.trim()) return;
    setIsLoading(true);
    const url = `http://localhost:9080/chat?query=${encodeURIComponent(question)}`;
    try {
      await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      await getConversations();
      setQuestion("");
    } catch (error) {
      console.error("Failed to submit question:", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleGenerateVideo(chatId, message) {
    setGeneratingVideos(prev => ({ ...prev, [chatId]: true }));
    try {
      const response = await fetch("http://localhost:9080/generate-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message }),
      });
      const videoBlob = await response.blob();
      const videoUrl = URL.createObjectURL(videoBlob);
      setVideoUrls(prev => ({ ...prev, [chatId]: videoUrl }));
    } catch (error) {
      console.error("Failed to generate video:", error);
    } finally {
      setGeneratingVideos(prev => ({ ...prev, [chatId]: false }));
    }
  }

  return (
    <div className="flex items-center justify-center w-full h-screen bg-gray-100">
      <div className="w-full h-full bg-white shadow-xl overflow-hidden">
        <div className="flex flex-col h-[100vh]">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <div className="bg-indigo-100 p-4 mt-10 rounded-lg">
              <p className="text-indigo-800">
                Welcome to the Comedy Show! 🌟 I'm here to help you generate jokes. What type of jokes can I tell you today?
              </p>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {/* ... existing welcome message ... */}
              {chats.map(({ id, role, message }) => (
                <div key={id} className={`flex flex-col ${role === 'user' ? 'items-end' : 'items-start'}`}>
                {/* // <div key={id} className={`flex flex-col ${role === 'user' ? 'items-end' : 'items-start'}`}> */}
                  <div className={`max-w-[75%] p-3 rounded-lg ${role === 'user' ? 'bg-indigo-200 text-indigo-900' : 'bg-gray-200 text-gray-900'}`}>
                    {message}
                  </div>
                  {role !== 'user' && (
                    <>
                      {!videoUrls[id] && !generatingVideos[id] && (
                        <button
                          className="mt-2 px-3 py-1 bg-green-500 text-white rounded-full hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
                          onClick={() => handleGenerateVideo(id, message)}
                        >
                          Generate Video
                        </button>
                      )}
                      {generatingVideos[id] && (
                        <div className="mt-2 px-3 py-1 bg-yellow-500 text-white rounded-full">
                          Generating...
                        </div>
                      )}
                      {videoUrls[id] && (
                        <video className="mt-2 rounded-lg" width="320" controls>
                          <source src={videoUrls[id]} type="video/mp4" />
                          Your browser does not support the video tag.
                        </video>
                      )}
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
          <div className="p-4 border-t">
            <div className="flex space-x-2">
              <input
                className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Ask your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              />
              <button
                className={`px-4 py-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                onClick={handleSubmit}
                disabled={isLoading}
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;