import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { useState, useEffect } from "react";
import { ClientCard } from "@/components/ClientCard";
import { mockClients, mockInternalProjects } from "@/data/mockClients";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

const Index = () => {
  const [displayedText, setDisplayedText] = useState("");
  const [organizationType, setOrganizationType] = useState<"client" | "internal">("client");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  //const fullText = "When a new buyer takes over an account, they have zero context. The supplier is frustrated explaining everything again. TicTacTo captures every email, call, and meeting to build an intelligent timeline with instant search. But here's the difference: we make data accessible in multiple forms—because every person consumes information differently. Choose between Chatbot, Knowledge Graph, Avatar, or Reels.";
  



  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-6 pt-32 pb-24 max-w-7xl">
        <div className="text-center space-y-8 animate-fade-in">
          <h1 className="text-6xl md:text-8xl font-bold text-foreground leading-none text-balance max-w-5xl mx-auto">
            The shared brain for every business.
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground font-light max-w-2xl mx-auto">
            Nothing gets lost. Context moves with people.
          </p>
        </div>
      </section>

      {/* Organizations Section */}
      <section className="container mx-auto px-6 py-24 max-w-7xl">
        <div className="space-y-12">
          <div className="text-center space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              Eco-system
            </h2>
            <p className="text-xl text-muted-foreground font-light max-w-2xl mx-auto">
              Select an organization to access their context
            </p>
          </div>

          {/* Two Column Layout */}
          <div className="grid md:grid-cols-2 gap-16 relative">
            {/* Clients Column */}
            <div className="space-y-6 pr-8">
              <h3 className="text-2xl font-semibold text-foreground text-center">Clients</h3>
              <div className="space-y-6">
                {/* TODO: Replace mockClients with real data from API/database */}
                {/* Example API call: const clients = await fetchClients(); */}
                {mockClients.map((client) => (
                  <ClientCard key={client.id} client={client} />
                ))}
              </div>
            </div>

            {/* Vertical Separator */}
            <div className="hidden md:block absolute left-1/2 top-0 bottom-0 w-[2px] bg-border -translate-x-1/2 shadow-sm" />

            {/* Internal Information Column */}
            <div className="space-y-6 pl-8">
              <h3 className="text-2xl font-semibold text-foreground text-center">Internal Knowledge</h3>
              <div className="space-y-6">
                {/* TODO: Replace mockInternalProjects with real data from API/database */}
                {/* Example API call: const projects = await fetchInternalProjects(); */}
                {mockInternalProjects.map((project) => (
                  <ClientCard key={project.id} client={project} />
                ))}
              </div>
            </div>
          </div>

          {/* Add Organization Button */}
          <div className="flex justify-center pt-8">
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button 
                  size="lg"
                  className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium gap-2"
                >
                  <Plus className="w-5 h-5" />
                  Add Organization
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New Organization</DialogTitle>
                  <DialogDescription>
                    Choose the type of organization and share your data to get started.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-6 pt-4">
                  <div className="space-y-3">
                    <Label>Organization Type</Label>
                    <RadioGroup value={organizationType} onValueChange={(value) => setOrganizationType(value as "client" | "internal")}>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="client" id="client" />
                        <Label htmlFor="client" className="font-normal cursor-pointer">Client Organization</Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <RadioGroupItem value="internal" id="internal" />
                        <Label htmlFor="internal" className="font-normal cursor-pointer">Internal Project</Label>
                      </div>
                    </RadioGroup>
                  </div>
                  
                  <div className="space-y-3">
                    <Label>Share Your Data</Label>
                    <div className="p-4 border border-border rounded-lg bg-muted/50">
                      <p className="text-sm text-muted-foreground">
                        {organizationType === "client" 
                          ? "Upload client data including emails, calls, and meeting notes to build their relationship intelligence."
                          : "Upload internal project data to track team activities and project health."}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button variant="outline" onClick={() => setIsDialogOpen(false)} className="flex-1">
                      Cancel
                    </Button>
                    <Button onClick={() => setIsDialogOpen(false)} className="flex-1">
                      Continue
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="problem" className="container mx-auto px-6 py-32 max-w-7xl">
        <div className="border-t border-border pt-32">
          <div className="grid md:grid-cols-2 gap-16">
            <div className="space-y-6">
              <h2 className="text-5xl md:text-6xl font-bold text-foreground leading-tight">
                When people leave, knowledge leaves.
              </h2>
              <p className="text-xl text-muted-foreground font-light leading-relaxed">
                Every handover is incomplete. Every new hire starts from zero. 
                Context scatters across emails, calls, and memory. The cost is invisible—until it's not.
              </p>
            </div>
            <div className="hidden md:block"></div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-32 max-w-7xl">
        <div className="border-t border-border pt-32">
          <div className="text-center space-y-8">
            <h2 className="text-5xl md:text-6xl font-bold text-foreground leading-tight max-w-3xl mx-auto">
              Make every relationship unforgettable.
            </h2>
            <div className="pt-4">
              <Button 
                size="lg" 
                className="bg-primary text-primary-foreground hover:bg-primary/90 px-8 h-12 text-base font-medium"
              >
                Get Early Access
              </Button>
            </div>
            <p className="text-muted-foreground font-light pt-4">
              Built for teams who never want to start over.
            </p>
          </div>
        </div>
      </section>

      {/* Footer spacer */}
      <div className="h-24"></div>
    </div>
  );
};

export default Index;