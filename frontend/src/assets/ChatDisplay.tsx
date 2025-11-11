import React from 'react';

// Định nghĩa type cho tin nhắn
type Message = {
  from: 'user' | 'bot';
  text: string;
};

// Định nghĩa props mà component này sẽ nhận từ App.jsx
interface ChatDisplayProps {
  messages: Message[]; // Nhận 1 array tin nhắn
  isLoading: boolean;  // Nhận trạng thái loading
}

// Đây là component chỉ để HIỂN THỊ
function ChatDisplay({ messages, isLoading }: ChatDisplayProps) {
  return (
    // Cái div này sẽ tự động cuộn (overflow-y-auto)
    // flex-1 để nó lấp đầy không gian
    <div className="flex-1 overflow-y-auto mb-4 space-y-4 p-4 border rounded-lg">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`p-2 rounded-lg ${
            msg.from === 'user' 
              ? 'bg-blue-100 ml-auto' 
              : 'bg-gray-100'
          } max-w-[80%]`}
        >
          {msg.text}
        </div>
      ))}
      {isLoading && (
        <div className="bg-gray-100 p-2 rounded-lg max-w-[80%]">
          <span className="animate-pulse">...</span>
        </div>
      )}
    </div>
  );
}

export default ChatDisplay;