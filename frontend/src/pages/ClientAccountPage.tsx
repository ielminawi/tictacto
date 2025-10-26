// import { useParams, useNavigate } from "react-router-dom";
// import RelationshipChatPanel from "@/components/RelationshipChatPanel";
// import { User, GitBranch, Video } from "lucide-react";
// import React from "react";

// export default function ClientAccountPage() {
//   const { clientId } = useParams<{ clientId: string }>();
//   const navigate = useNavigate();

//   // Extract context from URL path as fallback
//   const currentPath = window.location.pathname;
//   const extractedContext = currentPath.includes("/client/")
//     ? currentPath.split("/client/")[1]?.split("/")[0]
//     : null;

//   const contextualClientIdRaw = clientId || extractedContext || "tacto";

//   // Directory of known clients
//   // Put your logos in /public/logos/... or adjust paths to match your setup
//   const clientDirectory: Record<
//     string,
//     {
//       name: string;
//       logo: string; // path to image
//       dataPoints: number;
//       healthPct: number;
//     }
//   > = {
//     tacto: {
//       name: "Tacto",
//       logo: "/images/tacto.png",
//       dataPoints: 1247,
//       healthPct: 85,
//     },
//     techparts: {
//       name: "TechParts GmbH",
//       logo: "/logos/techparts.png",
//       dataPoints: 972,
//       healthPct: 72,
//     },
//     altus: {
//       name: "Altus Components",
//       logo: "/logos/altus.png",
//       dataPoints: 563,
//       healthPct: 64,
//     },
//     // add more clients here
//   };

//   // normalize key (in case someone hits /client/Tacto vs /client/tacto)
//   const contextualKey = contextualClientIdRaw.toLowerCase();

//   const clientRecord = clientDirectory[contextualKey] || {
//     name: contextualClientIdRaw,
//     logo: "", // fallback -> we'll render placeholder
//     dataPoints: 1247,
//     healthPct: 85,
//   };

//   // Mock data – replace later with backend data
//   const recentUpdates = [
//     {
//       text: "Alex unhappy with price change",
//       source: "Outlook",
//       ago: "47 minutes ago",
//       tone: "chill",
//     },
//     {
//       text: "Andre going on vacation until 22nd of November",
//       source: "Teams meeting transcription",
//       ago: "3 days ago",
//       tone: "icy",
//     },
//     {
//       text: "PO-442 delay triggered escalation to Martin",
//       source: "Call notes",
//       ago: "6 days ago",
//       tone: "ganja",
//     },
//   ];

//   // Accent palette for recent activity rows
//   const toneStyles: Record<
//     string,
//     {
//       textClass: string;
//       pillClass: string;
//       timeClass: string;
//     }
//   > = {
//     hot: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-red-400 border-red-400/40 bg-red-950/20",
//       timeClass: "text-red-400",
//     },
//     warm: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-yellow-400 border-yellow-400/40 bg-yellow-950/20",
//       timeClass: "text-yellow-400",
//     },
//     cool: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-muted-foreground border-border bg-card/40",
//       timeClass: "text-muted-foreground",
//     },
//     chill: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-blue-400 border-blue-400/40 bg-blue-950/20",
//       timeClass: "text-blue-400",
//     },
//     icy: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-purple-400 border-purple-400/40 bg-purple-950/20",
//       timeClass: "text-purple-400",
//     },
//     ganja: {
//       textClass: "text-foreground",
//       pillClass:
//         "text-green-400 border-green-400/40 bg-green-950/20",
//       timeClass: "text-green-400",
//     },
//   };

//   const handleBackClick = () => {
//     // send user back to the clients list page
//     navigate("/");
//     // if you'd rather just go browser-back instead of a fixed route:
//     // navigate(-1);
//   };

//   return (
//     <div className="min-h-screen bg-background text-foreground">
//       <section className="px-6 pt-8 pb-24 max-w-[1400px] mx-auto">
//         {/* 2-column layout: main content + chat panel */}
//         <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
//           {/* LEFT SIDE */}
//           <div className="flex flex-col">
//             {/* HEADER */}
//             <div className="mb-10">
//               {/* back link */}
//               <button
//                 onClick={handleBackClick}
//                 className="text-sm text-muted-foreground flex items-center gap-2 hover:text-foreground transition-colors"
//               >
//                 <span className="text-lg leading-none">←</span>
//                 <span>Back to Clients</span>
//               </button>

//               <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6 mt-6">
//                 {/* left cluster: logo + name + metrics */}
//                 <div className="flex items-start gap-4">
//                   {/* logo or fallback box */}
//                   {clientRecord.logo ? (
//                     <div className="w-14 h-14 rounded-md border border-border bg-card flex items-center justify-center overflow-hidden">
//                       <img
//                         src={clientRecord.logo}
//                         alt={clientRecord.name}
//                         className="w-full h-full object-contain p-2"
//                       />
//                     </div>
//                   ) : (
//                     <div className="w-14 h-14 rounded-md border border-border bg-card flex items-center justify-center text-xs text-muted-foreground">
//                       +
//                     </div>
//                   )}

//                   <div className="space-y-2">
//                     {/* company name */}
//                     <div className="text-3xl font-semibold leading-tight">
//                       {clientRecord.name}
//                     </div>

//                     <div className="flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
//                       <div className="flex flex-col">
//                         <span className="uppercase text-[10px] tracking-wide text-muted-foreground">
//                           Data Points
//                         </span>
//                         <span className="text-base font-medium text-foreground">
//                           {clientRecord.dataPoints.toLocaleString("en-US")}
//                         </span>
//                       </div>

//                       <div className="flex flex-col">
//                         <span className="uppercase text-[10px] tracking-wide text-muted-foreground">
//                           Relationship Health
//                         </span>
//                         <span
//                           className={`text-base font-medium ${
//                             clientRecord.healthPct >= 80
//                               ? "text-green-500"
//                               : clientRecord.healthPct >= 60
//                               ? "text-yellow-400"
//                               : "text-red-500"
//                           }`}
//                         >
//                           {clientRecord.healthPct}%
//                         </span>
//                       </div>
//                     </div>
//                   </div>
//                 </div>
//               </div>
//             </div>

//             {/* RECENT UPDATES CARD */}
//             <div className="bg-card border border-border rounded-lg p-6 mb-10">
//               <div className="text-base font-medium text-foreground mb-4">
//                 Latest activity
//               </div>

//               <div className="space-y-4">
//                 {recentUpdates.map((item, idx) => {
//                   const tone = toneStyles[item.tone] || toneStyles.cool;
//                   return (
//                     <div
//                       key={idx}
//                       className="flex flex-col sm:flex-row sm:items-baseline sm:justify-between"
//                     >
//                       {/* left side text + source pill */}
//                       <div
//                         className={`text-sm leading-relaxed ${tone.textClass}`}
//                       >
//                         <span className="font-normal">{item.text}</span>{" "}
//                         <span
//                           className={`inline-block text-[10px] leading-none px-2 py-1 rounded border ${tone.pillClass}`}
//                         >
//                           {item.source}
//                         </span>
//                       </div>

//                       {/* time ago */}
//                       <div
//                         className={`text-xs mt-1 sm:mt-0 ${tone.timeClass}`}
//                       >
//                         {item.ago}
//                       </div>
//                     </div>
//                   );
//                 })}
//               </div>
//             </div>

//             {/* ACCESS MODES SECTION */}
//             <div className="mb-6">
//               <div className="text-xl font-medium text-foreground mb-4">
//                 How would you like to access this data?
//               </div>

//               <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//                 {/* Avatar */}
//                 <button
//                   className="
//                     bg-card border border-border rounded-lg p-5 text-left
//                     hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
//                     transition-all duration-150 ease-out
//                     cursor-pointer group
//                   "
//                 >
//                   <div className="flex items-start gap-3 mb-2">
//                     <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
//                       <User className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
//                     </div>
//                     <div className="text-base font-medium text-foreground">
//                       Avatar
//                     </div>
//                   </div>
//                   <div className="text-sm text-muted-foreground leading-relaxed">
//                     Meet an AI persona that embodies your{" "}
//                     {clientRecord.name} account knowledge.
//                   </div>
//                 </button>

//                 {/* Knowledge Graph */}
//                 <button
//                   className="
//                     bg-card border border-border rounded-lg p-5 text-left
//                     hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
//                     transition-all duration-150 ease-out
//                     cursor-pointer group
//                   "
//                 >
//                   <div className="flex items-start gap-3 mb-2">
//                     <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
//                       <GitBranch className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
//                     </div>
//                     <div className="text-base font-medium text-foreground">
//                       Knowledge Graph
//                     </div>
//                   </div>
//                   <div className="text-sm text-muted-foreground leading-relaxed">
//                     Visualize connections and decisions in your{" "}
//                     {clientRecord.name} relationship.
//                   </div>
//                 </button>

//                 {/* Reels */}
//                 <button
//                   className="
//                     bg-card border border-border rounded-lg p-5 text-left
//                     hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
//                     transition-all duration-150 ease-out
//                     cursor-pointer group
//                   "
//                 >
//                   <div className="flex items-start gap-3 mb-2">
//                     <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
//                       <Video className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
//                     </div>
//                     <div className="text-base font-medium text-foreground">
//                       Reels
//                     </div>
//                   </div>
//                   <div className="text-sm text-muted-foreground leading-relaxed">
//                     Watch your {clientRecord.name} relationship history
//                     unfold like a story.
//                   </div>
//                 </button>
//               </div>
//             </div>
//           </div>

//           {/* RIGHT SIDE CHAT */}
//           <div className="lg:sticky lg:top-8">
//             <RelationshipChatPanel companyId={contextualKey} />
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// }


import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import RelationshipChatPanel from "@/components/RelationshipChatPanel";
import { User, GitBranch, Video } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ClientAccountPage() {
  const { clientId } = useParams<{ clientId: string }>();
  const navigate = useNavigate();

  // modal toggle for knowledge graph overlay
  const [showGraph, setShowGraph] = useState(false);

  // Extract context from URL path as fallback
  const currentPath = window.location.pathname;
  const extractedContext = currentPath.includes("/client/")
    ? currentPath.split("/client/")[1]?.split("/")[0]
    : null;

  const contextualClientIdRaw = clientId || extractedContext || "tacto";

  // Directory of known clients
  const clientDirectory: Record<
    string,
    {
      name: string;
      logo: string; // path to image
      dataPoints: number;
      healthPct: number;
    }
  > = {
    tacto: {
      name: "Tacto",
      logo: "/images/tacto.png",
      dataPoints: 1247,
      healthPct: 85,
    },
    techparts: {
      name: "TechParts GmbH",
      logo: "/logos/techparts.png",
      dataPoints: 972,
      healthPct: 72,
    },
    altus: {
      name: "Altus Components",
      logo: "/logos/altus.png",
      dataPoints: 563,
      healthPct: 64,
    },
    // add more clients here
  };

  // normalize key (in case someone hits /client/Tacto vs /client/tacto)
  const contextualKey = contextualClientIdRaw.toLowerCase();

  const clientRecord = clientDirectory[contextualKey] || {
    name: contextualClientIdRaw,
    logo: "", // fallback -> we'll render placeholder
    dataPoints: 1247,
    healthPct: 85,
  };

  // Mock data – replace later with backend data
  const recentUpdates = [
    {
      text: "Alex unhappy with price change",
      source: "Outlook",
      ago: "47 minutes ago",
      tone: "chill",
    },
    {
      text: "Andre going on vacation until 22nd of November",
      source: "Teams meeting transcription",
      ago: "3 days ago",
      tone: "icy",
    },
    {
      text: "PO-442 delay triggered escalation to Martin",
      source: "Call notes",
      ago: "6 days ago",
      tone: "ganja",
    },
  ];

  // Accent palette for recent activity rows
  const toneStyles: Record<
    string,
    {
      textClass: string;
      pillClass: string;
      timeClass: string;
    }
  > = {
    hot: {
      textClass: "text-foreground",
      pillClass: "text-red-400 border-red-400/40 bg-red-950/20",
      timeClass: "text-red-400",
    },
    warm: {
      textClass: "text-foreground",
      pillClass: "text-yellow-400 border-yellow-400/40 bg-yellow-950/20",
      timeClass: "text-yellow-400",
    },
    cool: {
      textClass: "text-foreground",
      pillClass: "text-muted-foreground border-border bg-card/40",
      timeClass: "text-muted-foreground",
    },
    chill: {
      textClass: "text-foreground",
      pillClass: "text-blue-400 border-blue-400/40 bg-blue-950/20",
      timeClass: "text-blue-400",
    },
    icy: {
      textClass: "text-foreground",
      pillClass: "text-purple-400 border-purple-400/40 bg-purple-950/20",
      timeClass: "text-purple-400",
    },
    ganja: {
      textClass: "text-foreground",
      pillClass: "text-green-400 border-green-400/40 bg-green-950/20",
      timeClass: "text-green-400",
    },
  };

  const handleBackClick = () => {
    // send user back to the clients list page
    navigate("/");
    // if you'd rather just go browser-back: navigate(-1);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <section className="px-6 pt-8 pb-24 max-w-[1400px] mx-auto">
        {/* 2-column layout: main content + chat panel */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
          {/* LEFT SIDE */}
          <div className="flex flex-col">
            {/* HEADER */}
            <div className="mb-10">
              {/* back link */}
              <button
                onClick={handleBackClick}
                className="text-sm text-muted-foreground flex items-center gap-2 hover:text-foreground transition-colors"
              >
                <span className="text-lg leading-none">←</span>
                <span>Back to Clients</span>
              </button>

              <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6 mt-6">
                {/* left cluster: logo + name + metrics */}
                <div className="flex items-start gap-4">
                  {/* logo or fallback box */}
                  {clientRecord.logo ? (
                    <div className="w-14 h-14 rounded-md border border-border bg-card flex items-center justify-center overflow-hidden">
                      <img
                        src={clientRecord.logo}
                        alt={clientRecord.name}
                        className="w-full h-full object-contain p-2"
                      />
                    </div>
                  ) : (
                    <div className="w-14 h-14 rounded-md border border-border bg-card flex items-center justify-center text-xs text-muted-foreground">
                      +
                    </div>
                  )}

                  <div className="space-y-2">
                    {/* company name */}
                    <div className="text-3xl font-semibold leading-tight">
                      {clientRecord.name}
                    </div>

                    <div className="flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
                      <div className="flex flex-col">
                        <span className="uppercase text-[10px] tracking-wide text-muted-foreground">
                          Data Points
                        </span>
                        <span className="text-base font-medium text-foreground">
                          {clientRecord.dataPoints.toLocaleString("en-US")}
                        </span>
                      </div>

                      <div className="flex flex-col">
                        <span className="uppercase text-[10px] tracking-wide text-muted-foreground">
                          Relationship Health
                        </span>
                        <span
                          className={`text-base font-medium ${
                            clientRecord.healthPct >= 80
                              ? "text-green-500"
                              : clientRecord.healthPct >= 60
                              ? "text-yellow-400"
                              : "text-red-500"
                          }`}
                        >
                          {clientRecord.healthPct}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* RECENT UPDATES CARD */}
            <div className="bg-card border border-border rounded-lg p-6 mb-10">
              <div className="text-base font-medium text-foreground mb-4">
                Latest activity
              </div>

              <div className="space-y-4">
                {recentUpdates.map((item, idx) => {
                  const tone = toneStyles[item.tone] || toneStyles.cool;
                  return (
                    <div
                      key={idx}
                      className="flex flex-col sm:flex-row sm:items-baseline sm:justify-between"
                    >
                      {/* left side text + source pill */}
                      <div
                        className={`text-sm leading-relaxed ${tone.textClass}`}
                      >
                        <span className="font-normal">{item.text}</span>{" "}
                        <span
                          className={`inline-block text-[10px] leading-none px-2 py-1 rounded border ${tone.pillClass}`}
                        >
                          {item.source}
                        </span>
                      </div>

                      {/* time ago */}
                      <div
                        className={`text-xs mt-1 sm:mt-0 ${tone.timeClass}`}
                      >
                        {item.ago}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* ACCESS MODES SECTION */}
            <div className="mb-6">
              <div className="text-xl font-medium text-foreground mb-4">
                How would you like to access this data?
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Avatar */}
                <button
                  className="
                    bg-card border border-border rounded-lg p-5 text-left
                    hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
                    transition-all duration-150 ease-out
                    cursor-pointer group
                  "
                >
                  <div className="flex items-start gap-3 mb-2">
                    <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
                      <User className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                    </div>
                    <div className="text-base font-medium text-foreground">
                      Avatar
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground leading-relaxed">
                    Meet an AI persona that embodies your {clientRecord.name}{" "}
                    account knowledge.
                  </div>
                </button>

                {/* Knowledge Graph */}
                <button
                  className="
                    bg-card border border-border rounded-lg p-5 text-left
                    hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
                    transition-all duration-150 ease-out
                    cursor-pointer group
                  "
                  onClick={() => setShowGraph(true)}
                >
                  <div className="flex items-start gap-3 mb-2">
                    <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
                      <GitBranch className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                    </div>
                    <div className="text-base font-medium text-foreground">
                      Knowledge Graph
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground leading-relaxed">
                    Visualize connections and decisions in your{" "}
                    {clientRecord.name} relationship.
                  </div>
                </button>

                {/* Reels */}
                <button
                  className="
                    bg-card border border-border rounded-lg p-5 text-left
                    hover:bg-card/80 hover:shadow-lg hover:-translate-y-0.5
                    transition-all duration-150 ease-out
                    cursor-pointer group
                  "
                >
                  <div className="flex items-start gap-3 mb-2">
                    <div className="rounded-md border border-border bg-background/20 p-2 group-hover:border-foreground/40 transition-colors">
                      <Video className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                    </div>
                    <div className="text-base font-medium text-foreground">
                      Reels
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground leading-relaxed">
                    Watch your {clientRecord.name} relationship history unfold
                    like a story.
                  </div>
                </button>
              </div>
            </div>
          </div>

          {/* RIGHT SIDE CHAT */}
          <div className="lg:sticky lg:top-8">
            <RelationshipChatPanel companyId={contextualKey} />
          </div>
        </div>
      </section>

      {/* KNOWLEDGE GRAPH OVERLAY MODAL */}
      {showGraph && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card border border-border rounded-lg w-full max-w-5xl h-[80vh] flex flex-col overflow-hidden shadow-2xl">
            {/* header */}
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="text-sm font-medium text-foreground">
                Knowledge Graph
              </div>
              <Button
                variant="outline"
                className="h-8 text-xs px-3"
                onClick={() => setShowGraph(false)}
              >
                Close
              </Button>
            </div>

            {/* iframe body */}
            <div className="flex-1 bg-background">
              <iframe
                src="/knowledge_graph.html"
                title="Knowledge Graph"
                className="w-full h-full border-0"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
