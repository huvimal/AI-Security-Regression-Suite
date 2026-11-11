"""Authorize simulated assistant proposals using server-owned state."""

DOCUMENTS = {"ops-handbook": "ops", "sales-handbook": "sales"}
MEMBERSHIPS = {"alice": "ops", "bao": "sales"}
APPROVALS = {"review-1": ("alice", "ops", "ticket-42", "close_ticket")}
TOOLS = {"read_document", "close_ticket"}


def decide(actor, workspace, proposal):
    if not isinstance(actor, str) or actor not in MEMBERSHIPS or MEMBERSHIPS[actor] != workspace:
        return "block", "workspace_access"
    if not isinstance(proposal, dict):
        return "block", "invalid_proposal"
    tool = proposal.get("tool")
    target = proposal.get("target")
    if not isinstance(tool, str) or tool not in TOOLS:
        return "block", "unknown_tool"
    if not isinstance(target, str):
        return "block", "invalid_target"
    if tool == "read_document":
        if DOCUMENTS.get(target) != workspace:
            return "block", "document_access"
        return "allow", "authorized_read"
    approval_id = proposal.get("approval_id")
    approval = APPROVALS.get(approval_id) if isinstance(approval_id, str) else None
    if approval != (actor, workspace, target, tool):
        return "block", "approval_required"
    return "allow", "authorized_action"
