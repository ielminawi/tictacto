import React, { useState } from "react";
import { Button } from "@/components/ui/button";

interface RelationshipChatPanelProps {
  companyId: string;
}

interface Message {
  from: "system" | "user" | "assistant";
  text: string;
}

export default function RelationshipChatPanel({ companyId }: RelationshipChatPanelProps) {
  const currentPath = window.location.pathname;
  const extractedContext = currentPath.includes("/client/")
    ? currentPath.split("/client/")[1]?.split("/")[0]
    : null;

  const contextualCompanyId = companyId || extractedContext || "techparts";

  const [messages, setMessages] = useState<Message[]>([
    {
      from: "system",
      text: `Ask me anything about ${contextualCompanyId}. Example: "What did we agree on payment terms?"`,
    },
  ]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage: Message = { from: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    // Add thinking message
    const thinkingMessage: Message = { from: "assistant", text: "Thinking..." };
    setMessages((prev) => [...prev, thinkingMessage]);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: userMessage.text,
          company_id: contextualCompanyId,
        }),
      });

      const data = await response.json();

      // Replace thinking message with actual response
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          from: "assistant",
          text: data.answer,
        };
        return newMessages;
      });
    } catch (error) {
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          from: "assistant",
          text: "Sorry, I couldn't process your request right now.",
        };
        return newMessages;
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[32rem] bg-card border border-border rounded-lg">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => {
          const isUser = message.from === "user";
          const isSystem = message.from === "system";

          const bubbleClasses = isUser
            ? "bg-[#e5e5e5] text-[#1a1a1a]" // light gray bubble
            : isSystem
            ? "bg-[#3b2a1a] border border-[#a9825f]/40 text-[#f2e6da]" // bronze for system
            : "bg-[#3b2a1a] border border-[#a9825f]/40 text-[#f2e6da]"; // bronze for assistant

          return (
            <div
              key={index}
              className={`flex ${isUser ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg shadow-sm ${bubbleClasses}`}
              >
                <div className="text-sm whitespace-pre-wrap">{message.text}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Input Row */}
      <div className="border-t border-border p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about this account..."
            disabled={loading}
            className="flex-1 border border-border rounded-md bg-background text-foreground text-sm px-3 py-2 outline-none focus:ring-2 focus:ring-[#a9825f]/50"
          />
          <Button
            onClick={handleSend}
            disabled={loading || !question.trim()}
            className="bg-[#e5e5e5] text-[#1a1a1a] hover:bg-[#d6d6d6] text-sm px-4"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}
