import { Button } from "@/components/ui/button";
import { MessageSquare } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Chatbot = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen">
      <section className="container mx-auto px-6 pt-32 pb-24 max-w-7xl">
        <Button 
          variant="outline" 
          onClick={() => navigate("/")}
          className="mb-8"
        >
          ← Back to Home
        </Button>
        
        <div className="space-y-12 animate-fade-in">
          <div className="flex items-center gap-6">
            <MessageSquare className="w-20 h-20 text-primary" strokeWidth={1.5} />
            <h1 className="text-6xl md:text-8xl font-bold text-foreground">
              Chatbot
            </h1>
          </div>

          <p className="text-2xl md:text-3xl text-muted-foreground font-light max-w-4xl">
            Ask anything about your relationship history. Get instant, context-aware answers.
          </p>

          <div className="space-y-8 pt-12">
            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Instant Knowledge Access
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Every conversation, decision, and detail is one question away. No more digging through emails or asking colleagues. Just ask the chatbot, and get the context you need instantly.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Context-Aware Responses
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                The chatbot understands the full history of your business relationships. It connects the dots between past interactions, decisions, and outcomes to give you meaningful answers.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Always Learning
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                As your relationships evolve, so does the chatbot's knowledge. Every new interaction enriches the shared brain, making future queries even more valuable.
              </p>
            </div>
          </div>

          <div className="pt-12">
            <Button 
              size="lg" 
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
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
