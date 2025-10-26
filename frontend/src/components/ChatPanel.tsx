import { Send, Building2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useState } from "react";
import type { Client } from "./ClientCard";

interface ChatPanelProps {
  client: Client;
}

export const ChatPanel = ({ client }: ChatPanelProps) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([
    {
      role: "assistant",
      content: `Hi! I'm here to help you with information about ${client.name}. What would you like to know?`
    }
  ]);

  const handleSend = () => {
    if (!message.trim()) return;

    setMessages([...messages, { role: "user", content: message }]);
    setMessage("");

    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: `I understand you're asking about "${message}". This is a demo response for ${client.name}.`
        }
      ]);
    }, 1000);
  };

  return (
    <div className="w-full md:w-[400px] bg-background border-l border-border flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 p-4 border-b border-border">
        <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center">
          {client.logo ? (
            <img src={client.logo} alt={client.name} className="w-6 h-6 object-contain" />
          ) : (
            <Building2 className="w-5 h-5 text-muted-foreground" />
          )}
        </div>
        <div>
          <h3 className="font-semibold text-foreground">{client.name}</h3>
          <p className="text-xs text-muted-foreground">AI Assistant</p>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-foreground"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                </div>
              </div>
            ))}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="p-4 border-t border-border">
          <div className="flex gap-2">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask anything..."
              className="flex-1"
            />
            <Button onClick={handleSend} size="icon">
              <Send className="h-4 w-4" />
            </Button>
        </div>
      </div>
    </div>
  );
};