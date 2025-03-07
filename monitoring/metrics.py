from flask import Flask, Response
import redis

app = Flask(__name__)


redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@app.route("/metrics")
def metrics():
    """
    Exposes custom Redis metrics in Prometheus format.
    """
    total_requests = redis_client.get("total_api_requests") or 0
    total_violations = redis_client.get("rate_limit_violations_total") or 0

    # Fetch top blocked clients
    blocked_clients = redis_client.zrangebyscore("blocked_clients", "-inf", "+inf", withscores=True)

    metrics_output = \
    f"""
    # HELP total_api_requests Total number of API requests
    # TYPE total_api_requests counter
    total_api_requests {total_requests}

    # HELP rate_limit_violations_total Total rate limit violations
    # TYPE rate_limit_violations_total counter
    rate_limit_violations_total {total_violations}
    """

    # Add blocked clients data
    for client, count in blocked_clients:
        metrics_output += \
        f"""
        # HELP blocked_clients_total Rate limit violations per client
        # TYPE blocked_clients_total counter
        blocked_clients_total{{client="{client}"}} {count}
        """

    return Response(metrics_output, mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
