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
  // Extract context from URL path as specified in instructions
  const currentPath = window.location.pathname;
  const extractedContext = currentPath.includes('/client/')
    ? currentPath.split('/client/')[1]?.split('/')[0]
    : null;

  const contextualCompanyId = companyId || extractedContext || "techparts";

  const [messages, setMessages] = useState<Message[]>([
    {
      from: "system",
      text: `Ask me anything about ${contextualCompanyId}. Example: "What did we agree on payment terms?"`
    }
  ]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage: Message = { from: "user", text: question };
    setMessages(prev => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    // Add thinking message
    const thinkingMessage: Message = { from: "assistant", text: "Thinking..." };
    setMessages(prev => [...prev, thinkingMessage]);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: userMessage.text,
          company_id: contextualCompanyId,
        })
      });

      const data = await response.json();

      // Replace thinking message with actual response
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = { from: "assistant", text: data.answer };
        return newMessages;
      });
    } catch (error) {
      // Replace thinking message with error
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          from: "assistant",
          text: "Sorry, I couldn't process your request right now."
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

  const handleBriefMe = () => {
    alert(`• Health: Yellow · Recoverable but fragile
• Q4 at risk: ~€420K
• Last escalation: PO-442 late twice → €7.2K credit
• How to talk to Martin: status first, apology last, call 16:30–18:00 CET`);
  };

  const handlePlayReel = () => {
    alert(`1. Q4 renewal at risk ~€420K
2. Threat: "We'll move half to Altus in Jan"
3. Thursday dispatch promise is critical
4. Never say "logistics backlog"
5. Call 16:30–18:00 CET`);
  };

  return (
    <div className="flex flex-col h-[32rem] bg-card border border-border rounded-lg">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.from === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                message.from === "user"
                  ? "bg-foreground text-background"
                  : message.from === "system"
                  ? "bg-muted text-foreground border border-dashed border-border"
                  : "bg-muted text-foreground border border-border"
              }`}
            >
              <div className="text-sm whitespace-pre-wrap">{message.text}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Input Row */}
      <div className="border-t border-border p-4">
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about this account..."
            disabled={loading}
            className="flex-1 border border-border rounded-md bg-background text-foreground text-sm px-3 py-2 outline-none focus:ring-2 focus:ring-primary/40"
          />
          <Button
            onClick={handleSend}
            disabled={loading || !question.trim()}
            className="bg-foreground text-background hover:bg-foreground/90 text-sm px-4"
          >
            Send
          </Button>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleBriefMe}
            className="text-xs"
          >
            Brief Me
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handlePlayReel}
            className="text-xs"
          >
            Play Reel
          </Button>
        </div>
      </div>
    </div>
  );
}