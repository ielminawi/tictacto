import { Button } from "@/components/ui/button";
import { User } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Avatar = () => {
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
            <User className="w-20 h-20 text-primary" strokeWidth={1.5} />
            <h1 className="text-6xl md:text-8xl font-bold text-foreground">
              Avatar
            </h1>
          </div>

          <p className="text-2xl md:text-3xl text-muted-foreground font-light max-w-4xl">
            Interact with an AI persona that embodies your account's knowledge and history.
          </p>

          <div className="space-y-8 pt-12">
            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Human-Like Interactions
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                The Avatar doesn't just answer questions—it engages in natural conversations. It understands context, tone, and nuance, making knowledge transfer feel personal and intuitive.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Embodies Your Relationships
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Each account has its own Avatar that represents the unique character and history of that business relationship. It's like having the perfect account manager who never forgets.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Continuous Memory
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                The Avatar remembers every interaction and evolves with your relationship. It bridges the gap when team members change, ensuring continuity and trust.
              </p>
            </div>
          </div>

          <div className="pt-12">
            <Button 
              size="lg" 
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
            >
              Meet Your Avatar
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Avatar;
