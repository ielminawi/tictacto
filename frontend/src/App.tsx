import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Chatbot from "./pages/Chatbot";
import Avatar from "./pages/Avatar";
import KnowledgeGraph from "./pages/KnowledgeGraph";
import Reels from "./pages/Reels";
import ClientDetail from "./pages/ClientDetail";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/client/:clientId" element={<ClientDetail />} />
          <Route path="/client/:clientId/chatbot" element={<Chatbot />} />
          <Route path="/client/:clientId/avatar" element={<Avatar />} />
          <Route path="/client/:clientId/knowledge-graph" element={<KnowledgeGraph />} />
          <Route path="/client/:clientId/reels" element={<Reels />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/avatar" element={<Avatar />} />
          <Route path="/knowledge-graph" element={<KnowledgeGraph />} />
          <Route path="/reels" element={<Reels />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
