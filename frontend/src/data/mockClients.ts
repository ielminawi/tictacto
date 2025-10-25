import { Client } from "@/components/ClientCard";
import productDevLogo from "@/assets/product-dev-logo.png";
import marketingLogo from "@/assets/marketing-logo.png";
import salesLogo from "@/assets/sales-logo.png";



// Mock client data for demonstration
// TODO: Replace with real data from database/API
// Expected data structure from backend:
// {
//   id: string (UUID from database)
//   name: string (organization name)
//   logo: string (URL to logo image)
//   healthScore: number (calculated from data completeness, activity, etc.)
//   dataPoints: number (count of emails, calls, meetings captured)
// }

export const mockClients: Client[] = [
  {
    id: "tacto",
    name: "Tacto",
    logo: "/images/tacto.png",
    healthScore: 85,
    dataPoints: 1247,
  },
  {
    id: "google",
    name: "Google",
    logo: "/images/google.png",
    healthScore: 92,
    dataPoints: 3891,
  },
  {
    id: "x",
    name: "X (Twitter)",
    logo: "/images/x.png",
    healthScore: 68,
    dataPoints: 892,
  },
  {
    id: "meta",
    name: "Meta",
    logo: "/images/meta.png",
    healthScore: 76,
    dataPoints: 2156,
  },
];

export const mockInternalProjects: Client[] = [
  {
    id: "product-dev",
    name: "Product Development",
    logo: productDevLogo,
    healthScore: 88,
    dataPoints: 2341,
  },
  {
    id: "marketing",
    name: "Marketing Team",
    logo: marketingLogo,
    healthScore: 72,
    dataPoints: 1567,
  },
  {
    id: "sales",
    name: "Sales Operations",
    logo: salesLogo,
    healthScore: 81,
    dataPoints: 1823,
  },
];

// Function to fetch real client data (to be implemented)
// export async function fetchClients(): Promise<Client[]> {
//   const response = await fetch('/api/clients');
//   return response.json();
// }

// Function to fetch real internal projects data (to be implemented)
// export async function fetchInternalProjects(): Promise<Client[]> {
//   const response = await fetch('/api/internal-projects');
//   return response.json();
// }
