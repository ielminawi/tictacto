import { Card } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { Building2 } from "lucide-react";

export interface Client {
  id: string;
  name: string;
  logo?: string;
  healthScore: number; // 0-100
  dataPoints: number;
}

interface ClientCardProps {
  client: Client;
}

export const ClientCard = ({ client }: ClientCardProps) => {
  const getHealthColor = (score: number) => {
    if (score >= 70) return "bg-green-500";
    if (score >= 40) return "bg-yellow-500";
    return "bg-red-500";
  };

  const getHealthLabel = (score: number) => {
    if (score >= 70) return "Healthy";
    if (score >= 40) return "Moderate";
    return "Low";
  };

  return (
    <Link to={`/client/${client.id}`}>
      <Card className="group relative p-8 bg-card rounded-lg border-2 border-border hover:border-primary transition-all duration-300 cursor-pointer overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        
        <div className="relative space-y-6">
          {/* Company Icon/Logo */}
          <div className="w-16 h-16 rounded-lg bg-muted flex items-center justify-center">
            {client.logo ? (
              <img src={client.logo} alt={client.name} className="w-12 h-12 object-contain" />
            ) : (
              <Building2 className="w-8 h-8 text-muted-foreground" />
            )}
          </div>

          {/* Company Name */}
          <h3 className="text-2xl font-semibold text-foreground">{client.name}</h3>

          {/* Data Points */}
          <p className="text-sm text-muted-foreground">
            {client.dataPoints.toLocaleString()} data points captured
          </p>

          {/* Health Status */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Relationship Health</span>
              <span className="font-medium text-foreground">{getHealthLabel(client.healthScore)}</span>
            </div>
            
            {/* Health Bar */}
            <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
              <div 
                className={`h-full ${getHealthColor(client.healthScore)} transition-all duration-500`}
                style={{ width: `${client.healthScore}%` }}
              />
            </div>
            
            <p className="text-xs text-muted-foreground">
              {client.healthScore}% complete
            </p>
          </div>
        </div>
      </Card>
    </Link>
  );
};
