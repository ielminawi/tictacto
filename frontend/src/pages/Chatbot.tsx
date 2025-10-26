import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { MessageSquare } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

type ChatMessage = {
  from: "system" | "user" | "assistant";
  text: string;
};

const Chatbot = () => {
  const navigate = useNavigate();
  const { clientId } = useParams<{ clientId: string }>();

  // Extract context from URL path as specified in instructions
  const currentPath = window.location.pathname;
  const extractedContext = currentPath.includes('/client/')
    ? currentPath.split('/client/')[1]?.split('/')[0]
    : null;

  const companyContext = clientId || extractedContext || "techparts";

  // chat state
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      from: "system",
      text:
        `Ask me anything about ${companyContext}. Example: "What did we agree on payment terms?"`,
    },
  ]);
  const [question, setQuestion] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // call backend /ask
  async function askBackend(q: string): Promise<string> {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: q,
        company_id: companyContext,
      }),
    });

    if (!res.ok) {
      console.error("Backend error", res.status);
      return "Sorry, I couldn't reach Relationship Memory.";
    }

    const data = await res.json();
    return data.answer ?? "No answer returned.";
  }

  async function handleSend() {
    if (!question.trim() || loading) return;

    const q = question.trim();
    setQuestion("");

    // optimistic update with user's message
    setMessages((prev) => [
      ...prev,
      { from: "user", text: q },
    ]);
    setLoading(true);

    // call backend
    let answerText: string;
    try {
      answerText = await askBackend(q);
    } catch (err) {
      console.error(err);
      answerText = "Sorry, something went wrong.";
    }

    // append assistant response
    setMessages((prev) => [
      ...prev,
      { from: "assistant", text: answerText },
    ]);

    setLoading(false);
  }

  return (
    <div className="min-h-screen">
      <section className="container mx-auto px-6 pt-32 pb-24 max-w-7xl">
        {/* back button */}
        <Button
          variant="outline"
          onClick={() => navigate("/")}
          className="mb-8"
        >
          ← Back to Home
        </Button>

        {/* header / hero copy */}
        <div className="space-y-12 animate-fade-in">
          <div className="flex items-center gap-6">
            <MessageSquare
              className="w-20 h-20 text-primary"
              strokeWidth={1.5}
            />
            <h1 className="text-6xl md:text-8xl font-bold text-foreground">
              Chatbot
            </h1>
          </div>

          <p className="text-2xl md:text-3xl text-muted-foreground font-light max-w-4xl">
            Ask anything about your relationship history. Get instant,
            context-aware answers.
          </p>

          {/* existing marketing blocks can stay above or move below the chat,
              but for demo impact we want the live chat UI visible here */}
          
          {/* LIVE CHAT PANEL */}
          <div className="pt-12 grid grid-cols-1 lg:grid-cols-2 gap-8 w-full">
            {/* LEFT SIDE: marketing / explanation */}
            <div className="space-y-8">
              <div className="bg-card border border-border rounded-lg p-8">
                <h2 className="text-3xl font-semibold text-foreground mb-4">
                  Instant Knowledge Access
                </h2>
                <p className="text-xl text-muted-foreground font-light leading-relaxed">
                  Every conversation, decision, and detail is one
                  question away. No more digging through emails or
                  asking colleagues. Just ask the chatbot, and get the
                  context you need instantly.
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-8">
                <h2 className="text-3xl font-semibold text-foreground mb-4">
                  Context-Aware Responses
                </h2>
                <p className="text-xl text-muted-foreground font-light leading-relaxed">
                  The chatbot understands the full history of your
                  business relationships. It connects the dots between
                  past interactions, decisions, and outcomes to give
                  you meaningful answers.
                </p>
              </div>

              <div className="bg-card border border-border rounded-lg p-8">
                <h2 className="text-3xl font-semibold text-foreground mb-4">
                  Always Learning
                </h2>
                <p className="text-xl text-muted-foreground font-light leading-relaxed">
                  As your relationships evolve, so does the shared
                  memory. Every new interaction enriches the brain,
                  making future queries even more valuable.
                </p>
              </div>
            </div>

            {/* RIGHT SIDE: actual working chat */}
            <div className="flex flex-col h-[32rem] bg-card border border-border rounded-lg">
              {/* message history */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      msg.from === "user"
                        ? "justify-end"
                        : "justify-start"
                    }`}
                  >
                    <div
                      className={`
                        max-w-[80%] rounded-xl px-4 py-3 text-sm leading-relaxed
                        ${
                          msg.from === "user"
                            ? "bg-foreground text-background"
                            : msg.from === "assistant"
                            ? "bg-muted text-foreground border border-border"
                            : "bg-muted text-foreground border border-dashed border-border"
                        }
                      `}
                      style={{ whiteSpace: "pre-line" }}
                    >
                      {msg.text}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="text-xs text-muted-foreground">
                    Thinking…
                  </div>
                )}
              </div>

              {/* input row */}
              <div className="border-t border-border p-4">
                <div className="flex gap-2">
                  <input
                    className="flex-1 border border-border rounded-md bg-background text-foreground text-sm px-3 py-2 outline-none focus:ring-2 focus:ring-primary/40"
                    placeholder='Ask: “What did we agree on payment terms?”'
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleSend();
                    }}
                  />
                  <Button
                    className="bg-foreground text-background hover:bg-foreground/90 text-sm px-4"
                    onClick={handleSend}
                    disabled={loading}
                  >
                    Send
                  </Button>
                </div>

                {/* action buttons under input */}
                <div className="flex gap-2 mt-4">
                  <Button
                    variant="outline"
                    className="flex-1 text-sm h-10"
                    onClick={() => {
                      // TODO: open Brief Me drawer modal
                      alert(
                        "Brief Me: Summary of health, money at risk, last escalation, how to talk to Martin."
                      );
                    }}
                  >
                    Brief Me
                  </Button>

                  <Button
                    variant="outline"
                    className="flex-1 text-sm h-10"
                    onClick={() => {
                      // TODO: open Reel modal
                      alert(
                        "Play Reel: 30s recap — Q4 at risk €420K, Altus threat, Thursday dispatch promise."
                      );
                    }}
                  >
                    Play Reel
                  </Button>
                </div>
              </div>
            </div>
          </div>

          {/* CTA stays if you want it */}
          <div className="pt-12">
            <Button
              size="lg"
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
              onClick={() => {
                // optional: scroll to chat panel
                const chatSection = document.querySelector(
                  ".h-[32rem]"
                );
                if (chatSection) {
                  chatSection.scrollIntoView({ behavior: "smooth" });
                }
              }}
            >
              Try Chatbot Demo
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Chatbot;
