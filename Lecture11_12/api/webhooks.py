from flask import Blueprint, request, jsonify
import logging

webhooks_bp = Blueprint('webhooks', __name__)
logger = logging.getLogger(__name__)

# ==========================================
# Event-driven Architecture & Webhooks (Ch 12-15)
# ==========================================

def send_notification(event_type, payload):
    """Simulate a notification system sending emails/alerts"""
    print(f"[NOTIFICATION SYSTEM] Event Triggered: {event_type}")
    print(f"[NOTIFICATION SYSTEM] Payload Data: {payload}")
    # In a real system, this would push to a message broker (RabbitMQ/Kafka) or call an email API

@webhooks_bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    """Receive webhooks from Stripe (e.g. payment_intent.succeeded)"""
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid payload"}), 400
        
    event_type = payload.get('type')
    
    if event_type == 'payment_intent.succeeded':
        # Simulated logic for updating order status based on payment success
        payment_data = payload.get('data', {}).get('object', {})
        amount = payment_data.get('amount')
        currency = payment_data.get('currency')
        
        send_notification("PAYMENT_SUCCESS", {"amount": amount, "currency": currency})
        
        return jsonify({"status": "success", "message": "Payment recorded"}), 200
        
    elif event_type == 'payment_intent.payment_failed':
        send_notification("PAYMENT_FAILED", payload)
        return jsonify({"status": "success", "message": "Payment failure recorded"}), 200
        
    return jsonify({"status": "ignored", "message": f"Unhandled event type {event_type}"}), 200


@webhooks_bp.route('/github', methods=['POST'])
def github_webhook():
    """Receive webhooks from GitHub (e.g. push, pull_request)"""
    # GitHub uses X-GitHub-Event header to denote event type
    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    payload = request.get_json()
    
    if event_type == 'push':
        commits = payload.get('commits', [])
        repo_name = payload.get('repository', {}).get('name', 'unknown')
        send_notification("CODE_PUSHED", {"repo": repo_name, "commits": len(commits)})
        return jsonify({"status": "success"}), 200
        
    elif event_type == 'pull_request':
        action = payload.get('action')
        pr_title = payload.get('pull_request', {}).get('title')
        send_notification("PULL_REQUEST", {"action": action, "title": pr_title})
        return jsonify({"status": "success"}), 200
        
    return jsonify({"status": "ignored"}), 200
