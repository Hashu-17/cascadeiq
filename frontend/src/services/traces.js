export async function fetchWorkflowTraces(workflowId) {
  const response = await fetch(`/api/workflows/${workflowId}/traces`);
  if (!response.ok) throw new Error('Unable to load traces');
  return response.json();
}
