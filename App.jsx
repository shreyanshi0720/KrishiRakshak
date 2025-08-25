import { useState, useRef, useEffect } from "react";

export default function AgroBuddyChatbot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", text: "नमस्ते 🙏! मैं आपकी किस प्रकार मदद कर सकता हूँ?" },
  ]);
  const [typing, setTyping] = useState(false);
  const [inputText, setInputText] = useState("");
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });

    // Initialize speech recognition
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        handleSend(transcript); // send voice message
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const handleSend = (text) => {
    if (!text || !text.trim()) return;

    setMessages([...messages, { sender: "user", text }]);
    setTyping(true);

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: `🌱 मैं आपकी किस प्रकार मदद कर सकता हूँ?` },
      ]);
      setTyping(false);
    }, 1000);

    setInputText(""); // clear input
  };

  const handleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert("Your browser does not support voice input.");
      return;
    }
    recognitionRef.current.start();
  };

  return (
    <>
      {/* Floating Button */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-green-600 hover:bg-green-700 p-6 rounded-full shadow-lg transition-transform hover:scale-110 animate-pulse"
          title="Chat with Agro Buddy"
        >
          🌾
        </button>
      )}

      {/* Chat Panel */}
      {open && (
        <div className="fixed top-0 right-0 z-50 h-full w-1/3 max-w-lg bg-white shadow-2xl flex flex-col">
          {/* Header */}
          <div className="bg-green-600 text-white flex justify-between items-center px-6 py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-400 rounded-full flex items-center justify-center text-white text-lg font-bold animate-bounce">
                🤖
              </div>
              <span className="font-semibold text-lg">Agro Buddy</span>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="text-white font-bold hover:text-gray-200 text-xl"
            >
              ✖
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-5 space-y-3 bg-yellow-50">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex items-start max-w-[80%] p-3 rounded-xl shadow-md ${
                  msg.sender === "user"
                    ? "ml-auto bg-gradient-to-r from-green-500 to-green-400 text-white"
                    : "mr-auto bg-gradient-to-r from-yellow-200 to-yellow-100 text-gray-800"
                }`}
              >
                <span>{msg.text}</span>
              </div>
            ))}

            {/* Typing Indicator */}
            {typing && (
              <div className="flex items-center space-x-1 mr-auto bg-yellow-200 p-2 rounded-xl w-16 animate-pulse">
                <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce"></span>
                <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce delay-150"></span>
                <span className="h-2 w-2 bg-green-500 rounded-full animate-bounce delay-300"></span>
              </div>
            )}

            <div ref={messagesEndRef}></div>
          </div>

          {/* Input */}
          <div className="flex items-center border-t p-3 bg-green-50">
            <input
              type="text"
              placeholder="Type a message..."
              className="flex-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-400 text-base"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSend(inputText);
              }}
            />
            <button
              onClick={() => handleSend(inputText)}
              className="ml-2 bg-green-600 hover:bg-green-700 text-white font-bold px-5 py-3 rounded-xl shadow transition-transform hover:scale-105"
            >
              ➤
            </button>
            <button
              onClick={handleVoiceInput}
              className="ml-2 bg-yellow-400 hover:bg-yellow-500 text-white font-bold px-4 py-3 rounded-xl shadow transition-transform hover:scale-105"
              title="Voice Input"
            >
              🎤
            </button>
          </div>
        </div>
      )}
    </>
  );
}

















