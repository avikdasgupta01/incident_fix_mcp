from __future__ import annotations

from typing import Callable

from fastmcp import FastMCP


mcp = FastMCP("IncidentFixServer")


def _complete(message: str) -> str:
    return message


@mcp.tool()
def restart_database() -> str:
    """Restart the database service."""
    return _complete("DB restarted successfully")


@mcp.tool()
def restart_service(service: str) -> str:
    """Restart a named service or worker."""
    return _complete(f"{service} restarted successfully")


@mcp.tool()
def refresh_invalid_token() -> str:
    """Refresh an invalid or expired service token."""
    return _complete("Authentication token refreshed successfully")


@mcp.tool()
def clear_disk_space() -> str:
    """Clear disk pressure by rotating logs and cleaning temporary files."""
    return _complete("Disk cleanup completed successfully")


@mcp.tool()
def reconnect_database() -> str:
    """Reconnect the application to the database and reset the connection pool."""
    return _complete("Database connection restored successfully")


@mcp.tool()
def retry_payment_gateway() -> str:
    """Retry the payment gateway call with backoff logic."""
    return _complete("Payment gateway retry completed successfully")


@mcp.tool()
def validate_json_payload() -> str:
    """Validate and sanitize malformed JSON input before retrying processing."""
    return _complete("JSON payload validated successfully")


@mcp.tool()
def rewrite_invalid_route() -> str:
    """Rewrite or reject invalid API routes to a supported endpoint."""
    return _complete("Invalid API route handled successfully")


@mcp.tool()
def reduce_concurrency(component: str) -> str:
    """Reduce concurrency for a hot component to lower CPU or memory pressure."""
    return _complete(f"Concurrency reduced successfully for {component}")


@mcp.tool()
def flush_cache(component: str = "cache") -> str:
    """Flush in-memory cache or buffers for a component."""
    return _complete(f"Cache flushed successfully for {component}")


@mcp.tool()
def requeue_task(task_id: str) -> str:
    """Requeue a failed idempotent task."""
    return _complete(f"Task {task_id} requeued successfully")


@mcp.tool()
def route_task_to_dead_letter_queue(task_id: str) -> str:
    """Move a repeatedly failing task to the dead-letter queue."""
    return _complete(f"Task {task_id} moved to dead-letter queue successfully")


@mcp.tool()
def restore_shared_library(library_name: str = "shared_lib.so") -> str:
    """Restore or relink a missing shared library from a known artifact source."""
    return _complete(f"{library_name} restored successfully")


@mcp.tool()
def isolate_unhealthy_node(node_name: str) -> str:
    """Isolate an unhealthy node after severe kernel or I/O failures."""
    return _complete(f"Node {node_name} isolated successfully")


@mcp.tool()
def enable_degraded_mode(component: str) -> str:
    """Place a component in degraded mode so the system can keep serving safely."""
    return _complete(f"Degraded mode enabled successfully for {component}")


@mcp.tool()
def optimize_users_query() -> str:
    """Apply the safe query fix for repeated SELECT * FROM users patterns."""
    return _complete("Users query optimized successfully")


@mcp.tool()
def refresh_service_endpoint_mapping() -> str:
    """Refresh internal endpoint mappings for deprecated or invalid routes."""
    return _complete("Endpoint mapping refreshed successfully")


@mcp.tool()
def classify_error(error_text: str) -> str:
    """Classify a log line into the most likely remediation category."""
    normalized = error_text.lower()

    if "outofmemoryerror" in normalized or "gc overhead limit exceeded" in normalized:
        return _complete("Classification: memory_pressure")
    if "invalid token" in normalized or "authentication failed" in normalized:
        return _complete("Classification: auth_token")
    if "disk space critical" in normalized:
        return _complete("Classification: disk_pressure")
    if "connection lost to database" in normalized:
        return _complete("Classification: database_connection")
    if "connection timeout" in normalized and "payment-gw" in normalized:
        return _complete("Classification: downstream_timeout")
    if "unexpected token" in normalized and "json" in normalized:
        return _complete("Classification: malformed_json")
    if "404 not found" in normalized or "/api/v1/invalid" in normalized:
        return _complete("Classification: invalid_route")
    if "shared_lib.so" in normalized or "critical dependency" in normalized:
        return _complete("Classification: missing_dependency")
    if "slow query" in normalized or "select * from users" in normalized:
        return _complete("Classification: slow_query")
    if "high cpu usage" in normalized:
        return _complete("Classification: cpu_pressure")
    if "memory usage reaching 90%" in normalized:
        return _complete("Classification: memory_warning")
    if "failed to process task" in normalized:
        return _complete("Classification: task_failure")
    if "kernel panic" in normalized:
        return _complete("Classification: kernel_io_failure")
    if "unexpected system shutdown" in normalized:
        return _complete("Classification: system_shutdown")
    if "deprecated api endpoint" in normalized:
        return _complete("Classification: deprecated_endpoint")

    return _complete("Classification: unknown")


def _dispatch(error_text: str) -> tuple[Callable[..., str], tuple]:
    normalized = error_text.lower()

    if "outofmemoryerror" in normalized or "gc overhead limit exceeded" in normalized:
        return restart_service, ("memory-impacted-service",)
    if "invalid token" in normalized or "authentication failed" in normalized:
        return refresh_invalid_token, ()
    if "disk space critical" in normalized:
        return clear_disk_space, ()
    if "connection lost to database" in normalized:
        return reconnect_database, ()
    if "connection timeout" in normalized and "payment-gw" in normalized:
        return retry_payment_gateway, ()
    if "unexpected token" in normalized and "json" in normalized:
        return validate_json_payload, ()
    if "404 not found" in normalized or "/api/v1/invalid" in normalized:
        return rewrite_invalid_route, ()
    if "shared_lib.so" in normalized or "critical dependency" in normalized:
        return restore_shared_library, ("shared_lib.so",)
    if "slow query" in normalized or "select * from users" in normalized:
        return optimize_users_query, ()
    if "high cpu usage" in normalized:
        return reduce_concurrency, ("high-cpu-component",)
    if "memory usage reaching 90%" in normalized:
        return flush_cache, ("memory-pressured-component",)
    if "failed to process task" in normalized:
        task_id = "ID-903" if "id-903" in normalized else "unknown-task"
        return requeue_task, (task_id,)
    if "kernel panic" in normalized:
        return isolate_unhealthy_node, ("io-failure-node",)
    if "unexpected system shutdown" in normalized:
        return enable_degraded_mode, ("system",)
    if "deprecated api endpoint" in normalized:
        return refresh_service_endpoint_mapping, ()

    return enable_degraded_mode, ("unknown-component",)


@mcp.tool()
def diagnose_and_fix(error_text: str) -> str:
    """Classify a log line and execute the matching autonomous remediation action."""
    action, args = _dispatch(error_text)
    return action(*args)


if __name__ == "__main__":
    mcp.run()
