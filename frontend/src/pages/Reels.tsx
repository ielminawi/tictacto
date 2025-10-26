import { Button } from "@/components/ui/button";
import { Video } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Reels = () => {
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
            <Video className="w-20 h-20 text-primary" strokeWidth={1.5} />
            <h1 className="text-6xl md:text-8xl font-bold text-foreground">
              Reels
            </h1>
          </div>

          <p className="text-2xl md:text-3xl text-muted-foreground font-light max-w-4xl">
            Watch your account history unfold like a story. Visual timelines that make complex relationships simple.
          </p>

          <div className="space-y-8 pt-12">
            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Story-Driven Context
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Reels transform your account history into a compelling narrative. See how relationships evolved over time, with key moments highlighted in an engaging, visual format.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Quick Onboarding
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                New team members can watch a Reel and understand years of relationship history in minutes. It's like watching a movie instead of reading a manual.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Visual Memory
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Some people learn better visually. Reels make information accessible to everyone, regardless of how they prefer to consume information.
              </p>
            </div>
          </div>

          <div className="pt-12">
            <Button 
              size="lg" 
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
            >
              Watch Demo Reel
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Reels;
