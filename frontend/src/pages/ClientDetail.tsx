import { Button } from "@/components/ui/button";
import { Video, User, Network, ArrowLeft, Building2 } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { mockClients } from "@/data/mockClients";
import { ChatPanel } from "@/components/ChatPanel";

const ClientDetail = () => {
  const { clientId } = useParams();
  
  // Find the client from mock data
  // TODO: Replace with API call to fetch real client data
  // const client = await fetchClientById(clientId);
  const client = mockClients.find(c => c.id === clientId);

  if (!client) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <h1 className="text-2xl font-bold">Client not found</h1>
          <Link to="/">
            <Button variant="outline">
              <ArrowLeft className="mr-2" />
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const getHealthColor = (score: number) => {
    if (score >= 70) return "text-green-500";
    if (score >= 40) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <div className="min-h-screen flex">
      {/* Main Content */}
      <div className="flex-1 overflow-auto">
      {/* Header */}
      <section className="container mx-auto px-6 pt-12 max-w-5xl">
        <Link to="/">
          <Button variant="ghost" size="sm" className="mb-8">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Clients
          </Button>
        </Link>

        {/* Company Overview */}
        <div className="space-y-8 animate-fade-in mb-16">
          <div className="flex items-start gap-6">
            <div className="w-24 h-24 rounded-xl bg-muted flex items-center justify-center">
              {client.logo ? (
                <img src={client.logo} alt={client.name} className="w-16 h-16 object-contain" />
              ) : (
                <Building2 className="w-12 h-12 text-muted-foreground" />
              )}
            </div>
            
            <div className="flex-1 space-y-4">
              <h1 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
                {client.name}
              </h1>
              
              <div className="flex items-center gap-8 text-muted-foreground">
                <div>
                  <span className="text-sm">Data Points</span>
                  <p className="text-2xl font-semibold text-foreground">
                    {client.dataPoints.toLocaleString()}
                  </p>
                </div>
                
                <div>
                  <span className="text-sm">Relationship Health</span>
                  <p className={`text-2xl font-semibold ${getHealthColor(client.healthScore)}`}>
                    {client.healthScore}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="max-w-3xl">
            <p className="text-xl text-muted-foreground font-light leading-relaxed">
              Access all relationship intelligence for {client.name}. Choose how you want to explore and interact with your shared business history.
            </p>
          </div>
        </div>
      </section>

      {/* Feature Navigation for this Client */}
      <section className="container mx-auto px-6 py-24 max-w-5xl">
        <h2 className="text-3xl font-bold text-foreground mb-8">
          How would you like to access this data?
        </h2>
        
        <div className="grid md:grid-cols-3 gap-6">
          <Link
            to={`/client/${clientId}/avatar`}
            className="group relative p-12 bg-card rounded-lg border-2 border-border hover:border-primary transition-all duration-300 text-left overflow-hidden block"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="relative space-y-4">
              <User className="w-12 h-12 text-foreground" strokeWidth={1.5} />
              <h3 className="text-2xl font-semibold text-foreground">Avatar</h3>
              <p className="text-muted-foreground font-light">Interact with an AI persona that embodies your {client.name} account knowledge.</p>
            </div>
          </Link>

          <Link
            to={`/client/${clientId}/knowledge-graph`}
            className="group relative p-12 bg-card rounded-lg border-2 border-border hover:border-primary transition-all duration-300 text-left overflow-hidden block"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="relative space-y-4">
              <Network className="w-12 h-12 text-foreground" strokeWidth={1.5} />
              <h3 className="text-2xl font-semibold text-foreground">Knowledge Graph</h3>
              <p className="text-muted-foreground font-light">Visualize connections and decisions in your {client.name} relationship.</p>
            </div>
          </Link>

          <Link
            to={`/client/${clientId}/reels`}
            className="group relative p-12 bg-card rounded-lg border-2 border-border hover:border-primary transition-all duration-300 text-left overflow-hidden block"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="relative space-y-4">
              <Video className="w-12 h-12 text-foreground" strokeWidth={1.5} />
              <h3 className="text-2xl font-semibold text-foreground">Reels</h3>
              <p className="text-muted-foreground font-light">Watch your {client.name} relationship history unfold like a story.</p>
            </div>
          </Link>
        </div>
      </section>

      {/* Footer spacer */}
      <div className="h-24"></div>
      </div>

      {/* Chat Panel - Always Visible */}
      <ChatPanel
        client={client}
      />
    </div>
  );
};

export default ClientDetail;
