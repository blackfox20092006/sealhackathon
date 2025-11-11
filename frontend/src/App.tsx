import { useState } from "react";
// import reactLogo from "./assets/react.svg"; // <-- Không dùng
// import viteLogo from "/vite.svg"; // <-- Không dùng
// import "./App.css";
// KHÔNG CẦN import ChatDisplay nữa

// === ĐỊNH NGHĨA TYPE (cho TypeScript) ===
type Message = {
  from: "user" | "bot";
  text: string;
};

// === COMPONENT APP (Component chính) ===
function App() {
  // --- STATE (Giữ nguyên) ---
  const [srsInput, setSrsInput] = useState("");
  const [srsMessages, setSrsMessages] = useState<Message[]>([]);
  const [srsIsLoading] = useState(false);

  const [utInput, setUtInput] = useState("");
  const [utMessages, setUtMessages] = useState<Message[]>([]);
  const [utIsLoading] = useState(false);

  const [agentInput, setAgentInput] = useState("");
  const [agentMessages, setAgentMessages] = useState<Message[]>([]);
  const [agentIsLoading, setAgentIsLoading] = useState(false);

  // --- CÁC HÀM (Giữ nguyên) ---
  const handleSrsSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const userMessage = srsInput;
    if (!userMessage.trim()) return;
    setSrsInput("");

    // Reset messages array and add only the new message
    setSrsMessages([{ from: "user", text: userMessage }]);
  };

  const handleUtSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const userMessage = utInput;
    if (!userMessage.trim()) return;
    setUtInput("");

    // Reset messages array and add only the new message
    setUtMessages([{ from: "user", text: userMessage }]);
  };

  const handleAgentSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const userMessage = agentInput;
    if (!userMessage.trim()) return;
    setAgentInput("");

    // Get the latest messages from all sections
    const lastSrsMessage = srsMessages.length > 0 
      ? srsMessages[srsMessages.length - 1].text 
      : "";

    const lastUtMessage = utMessages.length > 0 
      ? utMessages[utMessages.length - 1].text 
      : "";

    const lastAgentMessage = agentMessages.length > 0 
      ? agentMessages[agentMessages.length - 1].text 
      : "";

    // Create the JSON payload
    const payload = {
      srs_raw: lastSrsMessage,
      userstory_raw: lastUtMessage,

    };

    // Display the message first
    setAgentMessages((prev) => [...prev, { from: "user", text: userMessage }]);
    setAgentIsLoading(true);

    try {
      // Build payload expected by /handle_interaction
      const interactionPayload = {
        userpromt: userMessage,
        final_suggestions: lastAgentMessage || "",
        srs_raw: lastSrsMessage,
      };

      const response = await fetch("http://localhost:5000/handle_interaction", {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(interactionPayload),
      });

      console.log("/handle_interaction response:", response);
      if (response.ok) {
        const data = await response.json();
        // backend returns { "response": "..." }
        setAgentMessages((prev) => [...prev, { from: "bot", text: data.response }]);
      
      } else {
        
      }
    } catch (error) {
      console.error("fetch /handle_interaction error:", error);
      setAgentMessages((prev) => [
        ...prev,
        { from: "bot", text: `Lỗi: ${(error as Error).message}` },
      ]);
    } finally {
      setAgentIsLoading(false);
    }
  };

  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    chatType: string
  ) => {
    const file = e.target.files?.[0];
    if (file) {
      const newFileMessage = {
        from: "user" as const,
        text: `Đã tải lên file: ${file.name}`,
      };
      if (chatType === "srs") {
        setSrsMessages((prev) => [...prev, newFileMessage]);
      } else if (chatType === "ut") {
        setUtMessages((prev) => [...prev, newFileMessage]);
      } else if (chatType === "agent") {
        setAgentMessages((prev) => [...prev, newFileMessage]);
      }
    }
  };

  // --- PHẦN HIỂN THỊ (JSX) ---
  return (
    <div className="container max-w-full h-screen border-2 border-black flex">
      <div className="taskBar_Layout w-[5%] flex flex-col items-center justify-start gap-4 pt-3">
        <div className="logo w-full h-auto">
          <img src="https://tse3.mm.bing.net/th/id/OIP.H7B2zQa6tyItU1JR6pPcngHaEE?rs=1&pid=ImgDetMain&o=7&rm=3" alt="fptfpt" />
        </div>
        <button
          onClick={() => {
            // Reset all messages
            setSrsMessages([]);
            setUtMessages([]);
            setAgentMessages([]);
            // Reset all inputs
            setSrsInput("");
            setUtInput("");
            setAgentInput("");
          }}
          className="p-2 rounded-full hover:bg-orange-200 transition-colors bg-orange-600 my-3"
          title="Reset All"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6 text-white"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
            />
          </svg>
        </button>

        <button
          onClick={async () => {
            // Get last SRS message or use input if no messages
            const lastSrsMessage =
              srsMessages.length > 0
                ? srsMessages[srsMessages.length - 1].text
                : srsInput.trim();

            // Get current UT input
            const currentUtInput =
              utMessages.length > 0
                ? utMessages[utMessages.length - 1].text
                : utInput.trim();

            // Check if we have any content to send
            if (!lastSrsMessage && !currentUtInput) return;

            // Create combined message as JSON
            const combinedMessage = {
              srs_raw: lastSrsMessage,
              userstory_raw: currentUtInput,
            };

            // Add the combined message to Agent chat as formatted JSON
            const displayMessage = JSON.stringify(combinedMessage, null, 2);
            setAgentMessages((prev) => [
              ...prev,
              { from: "user", text: displayMessage },
            ]);
            setAgentIsLoading(true);

            try {
                const payload2 = {
                  srs_raw: lastSrsMessage,
                  userstory_raw: currentUtInput,
                };

                const response = await fetch("http://localhost:5000/process_suggestions", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(payload2),
                });

                if (!response.ok) {
                  const text = await response.text();
                  throw new Error(`process_suggestions failed: ${response.status} ${text}`);
                }

                const data = await response.json();

                const response2 = await fetch("http://localhost:5000/handle_translate", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ text: data.suggestions, target: "vi" }),
                });

                if (!response2.ok) {
                  const text = await response2.text();
                  throw new Error(`handle_translate failed: ${response2.status} ${text}`);
                }

                const translated = await response2.json();

                setAgentMessages((prev) => [
                  ...prev,
                  { from: "bot", text: translated.response },
                ]);
              } catch (error) {
                setAgentMessages((prev) => [
                  ...prev,
                  { from: "bot", text: `Lỗi: ${(error as Error).message}` },
                ]);
              } finally {
                setAgentIsLoading(false);
                setSrsInput("");
                setUtInput("");
            }
          }}
          className="p-2 rounded-full hover:bg-orange-200 transition-colors bg-orange-600"
          title="Send to AI Agent"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6 text-white"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.25 6.75 12 3m0 0 3.75 3.75M12 3v18"
            />
          </svg>
        </button>
      </div>

      <div className="Main_Layout flex w-[95%]">
        {/* === CỘT TRÁI: SRS VÀ UT === */}
        <div className="SRS_UT_Layout border-2 w-[45%] h-full">
          {/* === Box 1: SRS === */}
          <div className="SRS_Layout border-2 w-full h-[50%]">
            {/* === KHU VỰC HIỂN THỊ CHAT SRS (85%) === */}
            {/* THÊM: p-4 (padding) và overflow-y-auto (scroll) */}
            <div id="UT_prompt" className="h-[85%] w-full p-4 overflow-y-auto">
              <h1 className="text-center text-xl font-serif">SRS</h1>

              {/* === FIX: DÁN LOGIC MAP VÀO ĐÂY === */}
              {srsMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`my-2 p-2 rounded-lg ${
                    msg.from === "user"
                      ? "bg-orange-300 ml-auto"
                      : "bg-gray-100"
                  } max-w-[80%]`}
                >
                  {msg.text}
                </div>
              ))}
              {srsIsLoading && (
                <div className="bg-gray-100 p-2 rounded-lg max-w-[80%]">
                  <span className="animate-pulse">Thinking...</span>
                </div>
              )}
              {/* === HẾT PHẦN FIX === */}
            </div>

            {/* KHU VỰC FORM SRS (15%) */}
            <div className="flex h-[15%] px-5 w-full items-center justify-center">
              {/* KẾT NỐI FORM 1 (Giữ nguyên) */}
              <form
                onSubmit={handleSrsSubmit}
                className="flex h-full w-full items-center justify-center rounded-full p-3 border border-2 border-stone-800"
              >
                <label
                  htmlFor="file-upload-srs"
                  className="mr-3 flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 hover:bg-gray-300 cursor-pointer transition-colors"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth="2"
                    stroke="currentColor"
                    className="h-6 w-6 text-gray-600"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 4.5v15m7.5-7.5h-15"
                    />
                  </svg>
                </label>
                <input
                  id="file-upload-srs"
                  type="file"
                  className="hidden"
                  onChange={(e) => handleFileChange(e, "srs")}
                />

                <input
                  type="text"
                  placeholder="Input to SRS"
                  value={srsInput}
                  onChange={(e) => setSrsInput(e.target.value)}
                  className="flex-1 bg-transparent text-lg text-black placeholder-gray-400 outline-none border-none focus:ring-0"
                />

                <div className="ml-3 flex items-center space-x-3">
                  <button
                    type="submit"
                    className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-600 hover:bg-orange-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth="3"
                      stroke="currentColor"
                      className="h-6 w-6 text-white"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m4.5 15.75 7.5-7.5 7.5 7.5"
                      />
                    </svg>
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* === Box 2: UT === */}
          <div className="UT_Layout border-2 w-full h-[50%]">
            {/* === KHU VỰC HIỂN THỊ CHAT UT (85%) === */}
            <div id="UT_prompt" className="h-[85%] w-full p-4 overflow-y-auto">
              <h1 className="text-center text-xl font-serif">User Story</h1>

              {/* === FIX: DÁN LOGIC MAP VÀO ĐÂY === */}
              {utMessages.map((msg, index) => (
                <div
                  key={index}
                  className={`my-2 p-2 rounded-lg ${
                    msg.from === "user"
                      ? "bg-orange-300 ml-auto"
                      : "bg-gray-100"
                  } max-w-[80%]`}
                >
                  {msg.text}
                </div>
              ))}
              {utIsLoading && (
                <div className="bg-gray-100 p-2 rounded-lg max-w-[80%]">
                  <span className="animate-pulse">Thinking...</span>
                </div>
              )}
              {/* === HẾT PHẦN FIX === */}
            </div>

            {/* KHU VỰC FORM UT (15%) */}
            <div className="flex h-[15%] px-5 w-full items-center justify-center ">
              {/* KẾT NỐI FORM 2 (Giữ nguyên) */}
              <form
                onSubmit={handleUtSubmit}
                className="flex h-full w-full items-center justify-center rounded-full p-3 border border-2 border-stone-800"
              >
                <label
                  htmlFor="file-upload-ut"
                  className="mr-3 flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 hover:bg-gray-300 cursor-pointer transition-colors"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth="2"
                    stroke="currentColor"
                    className="h-6 w-6 text-gray-600"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 4.5v15m7.5-7.5h-15"
                    />
                  </svg>
                </label>
                <input
                  id="file-upload-ut"
                  type="file"
                  className="hidden"
                  onChange={(e) => handleFileChange(e, "ut")}
                />

                <input
                  type="text"
                  placeholder="Input to User Story"
                  value={utInput}
                  onChange={(e) => setUtInput(e.target.value)}
                  className="flex-1 bg-transparent text-lg text-black placeholder-gray-400 outline-none border-none focus:ring-0"
                />

                <div className="ml-3 flex items-center space-x-3">
                  <button
                    type="submit"
                    className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-600 hover:bg-orange-700"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth="3"
                      stroke="currentColor"
                      className="h-6 w-6 text-white"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="m4.5 15.75 7.5-7.5 7.5 7.5"
                      />
                    </svg>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        {/* === CỘT PHẢI: AI AGENT === */}
        <div className="AI_Agent_Layout border-2 w-[55%] h-full">
          {/* === KHU VỰC HIỂN THỊ CHAT AGENT (92%) === */}
          <div id="AI_prompt" className="h-[92%] w-full p-4 overflow-y-auto">
            <h1 className="text-center text-xl font-serif">AI Agent</h1>

            {/* === FIX: DÁN LOGIC MAP VÀO ĐÂY === */}
            {agentMessages.map((msg, index) => (
              <div
                key={index}
                className={`my-2 p-2 rounded-lg ${
                  msg.from === "user" ? "bg-orange-300 ml-auto" : "bg-gray-100"
                } max-w-[80%]`}
              >
                {msg.text}
              </div>
            ))}
            {agentIsLoading && (
              <div className="bg-gray-100 p-2 rounded-lg max-w-[80%]">
                <span className="animate-pulse">Thinking...</span>
              </div>
            )}
            {/* === HẾT PHẦN FIX === */}
          </div>

          {/* KHU VỰC FORM AGENT (8%) */}
          <div className="flex h-[8%] px-5 w-full items-center justify-center ">
            {/* KẾT NỐI FORM 3 (Giữ nguyên) */}
            <form
              onSubmit={handleAgentSubmit}
              className="flex h-full w-full items-center justify-center rounded-full p-3 border border-2 border-stone-800"
            >
              <label
                htmlFor="file-upload-agent"
                className="mr-3 flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 hover:bg-gray-300 cursor-pointer transition-colors"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="2"
                  stroke="currentColor"
                  className="h-6 w-6 text-gray-600"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4.5v15m7.5-7.5h-15"
                  />
                </svg>
              </label>
              <input
                id="file-upload-agent"
                type="file"
                className="hidden"
                onChange={(e) => handleFileChange(e, "agent")}
              />

              <input
                type="text"
                placeholder={srsMessages.length === 0 && utMessages.length === 0 
                  ? "Please add SRS and User Story first" 
                  : "Hỏi bất kỳ điều gì"}
                value={agentInput}
                onChange={(e) => setAgentInput(e.target.value)}
                disabled={srsMessages.length === 0 && utMessages.length === 0}
                className={`flex-1 bg-transparent text-lg text-black placeholder-gray-400 outline-none border-none focus:ring-0 
                  ${srsMessages.length === 0 && utMessages.length === 0 ? 'cursor-not-allowed opacity-50' : ''}`}
              />

              <div className="ml-3 flex items-center space-x-3">
                <button
                  type="submit"
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-600 hover:bg-orange-700"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth="3"
                    stroke="currentColor"
                    className="h-6 w-6 text-white"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="m4.5 15.75 7.5-7.5 7.5 7.5"
                    />
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
