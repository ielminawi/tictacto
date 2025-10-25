import { useParams } from "react-router-dom";
import RelationshipChatPanel from "@/components/RelationshipChatPanel";

export default function ClientAccountPage() {
  const { clientId } = useParams<{ clientId: string }>();

  // Extract context from URL path as specified in instructions
  const currentPath = window.location.pathname;
  const extractedContext = currentPath.includes('/client/')
    ? currentPath.split('/client/')[1]?.split('/')[0]
    : null;

  const contextualClientId = clientId || extractedContext || "techparts";

  return (
    <div className="min-h-screen bg-background text-foreground">
      <section className="container mx-auto px-6 pt-24 pb-24 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* LEFT COLUMN */}
          <div className="space-y-6">
            {/* Account Name */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                Account Name
              </div>
              <div className="text-2xl font-semibold mt-1">
                {contextualClientId}
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                Primary manufacturing partner for industrial components.
              </div>
            </div>

            {/* Relationship Health */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                Relationship Health
              </div>
              <div className="text-lg font-medium text-yellow-600 mt-1">
                Yellow · Recoverable but fragile
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                Renewal risk: Medium. Q4 at risk: ~€420K.
                Threat: "We'll move half to Altus Components in Jan if you slip again."
              </div>
            </div>

            {/* Renewal / Money at Risk */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                Renewal Risk
              </div>
              <div className="text-lg font-medium text-red-600 mt-1">
                ~€420K Q4 at Risk
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                Major threat: "We'll move half to Altus Components in Jan if you slip again."
                Thursday dispatch promise is critical to maintaining relationship.
              </div>
            </div>

            {/* Latest Escalation */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                Latest Escalation
              </div>
              <div className="text-lg font-medium text-orange-600 mt-1">
                PO-442 Late Twice
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                €7.2K credit issued. Thursday dispatch promise made.
                Martin escalated directly to leadership team.
              </div>
            </div>

            {/* Payment Terms */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                Payment Terms
              </div>
              <div className="text-lg font-medium mt-1">
                Net 30 vs Net 45 Dispute
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                Martin wants Net 30 vs our standard Net 45.
                Agreement is verbal only - needs documentation.
              </div>
            </div>

            {/* How to Talk to Martin */}
            <div className="bg-card border border-border rounded-lg p-6">
              <div className="text-xs text-muted-foreground uppercase tracking-wide">
                How to Talk to Martin
              </div>
              <div className="text-lg font-medium text-blue-600 mt-1">
                Communication Protocol
              </div>
              <div className="text-sm text-muted-foreground mt-3 leading-relaxed">
                Status first, fix second, apology last.
                Never say "logistics backlog".
                Best time to call: 16:30–18:00 CET.
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN */}
          <div>
            <RelationshipChatPanel companyId={contextualClientId} />
          </div>
        </div>
      </section>
    </div>
  );
}