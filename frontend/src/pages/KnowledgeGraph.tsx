import { Button } from "@/components/ui/button";
import { Network } from "lucide-react";
import { useNavigate } from "react-router-dom";

const KnowledgeGraph = () => {
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
            <Network className="w-20 h-20 text-primary" strokeWidth={1.5} />
            <h1 className="text-6xl md:text-8xl font-bold text-foreground">
              Knowledge Graph
            </h1>
          </div>

          <p className="text-2xl md:text-3xl text-muted-foreground font-light max-w-4xl">
            Visualize connections, decisions, and relationships in an interactive network.
          </p>

          <div className="space-y-8 pt-12">
            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                See the Big Picture
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Complex relationships become clear when visualized. The Knowledge Graph maps out connections between people, decisions, projects, and outcomes—showing you patterns that text can't reveal.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Interactive Exploration
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Navigate through your relationship history visually. Click on nodes to explore deeper, trace decision paths, and discover how different aspects of your business connect.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-12">
              <h2 className="text-3xl font-semibold text-foreground mb-6">
                Uncover Hidden Insights
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                The Knowledge Graph reveals connections you didn't know existed. Identify key influencers, understand decision chains, and spot opportunities that linear timelines miss.
              </p>
            </div>
          </div>

          <div className="pt-12">
            <Button 
              size="lg" 
              className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
            >
              Explore Knowledge Graph
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default KnowledgeGraph;
