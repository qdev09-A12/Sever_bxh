from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Bộ nhớ tạm: user -> điểm
users = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Thiếu tên"}), 400

    if name in users:
        return jsonify({"message": "Tên đã tồn tại", "points": users[name]}), 200

    users[name] = 0
    return jsonify({"message": "Đăng ký thành công", "points": 0}), 200


@app.route("/add_point", methods=["POST"])
def add_point():
    data = request.get_json()
    name = data.get("name")

    if not name or name not in users:
        return jsonify({"error": "Tài khoản chưa tồn tại"}), 400

    users[name] += 1
    return jsonify({"message": "Cộng điểm thành công", "points": users[name]}), 200


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
    top5 = sorted_users[:5]
    return jsonify([
        {"name": name, "points": points} for name, points in top5
    ])


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Replit sẽ tự set PORT
    app.run(host="0.0.0.0", port=port, debug=True)
