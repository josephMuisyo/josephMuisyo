from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from backend.cars import BRANDS, CARS_JSON

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
ALLOWED_PAYMENTS = {"cash", "bank transfer", "cheque", "hire purchase"}

ROUTES = {
    "/": "index.html",
    "/selection": "selection.html",
    "/checkout": "checkout.html",
}

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
}


class CarYardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/api/cars":
            self.send_json(
                HTTPStatus.OK,
                {
                    "total": len(CARS_JSON),
                    "brands": BRANDS,
                    "cars": CARS_JSON,
                },
            )
            return

        if parsed.path in ROUTES:
            self.serve_file(PUBLIC_DIR / ROUTES[parsed.path])
            return

        asset_path = (PUBLIC_DIR / parsed.path.lstrip("/")).resolve()
        if str(asset_path).startswith(str(PUBLIC_DIR.resolve())) and asset_path.exists():
            self.serve_file(asset_path)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/checkout":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            payload = json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Invalid JSON body."})
            return

        car_id = payload.get("carId")
        payment_method = payload.get("paymentMethod")
        deposit_percent = payload.get("depositPercent")

        if not car_id or not payment_method:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "carId and paymentMethod are required."})
            return

        if payment_method not in ALLOWED_PAYMENTS:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Unsupported payment method."})
            return

        selected_car = next((car for car in CARS_JSON if car["id"] == car_id), None)
        if not selected_car:
            self.send_json(HTTPStatus.NOT_FOUND, {"message": "Selected car was not found."})
            return

        if payment_method == "hire purchase":
            if not isinstance(deposit_percent, (int, float)):
                self.send_json(
                    HTTPStatus.BAD_REQUEST,
                    {"message": "Hire purchase requires a numeric depositPercent."},
                )
                return

            if deposit_percent < 30:
                self.send_json(
                    HTTPStatus.BAD_REQUEST,
                    {"message": "Hire purchase deposit must be at least 30 percent of the car value."},
                )
                return

        self.send_json(
            HTTPStatus.OK,
            {
                "message": "Checkout accepted.",
                "selectedCar": selected_car,
                "paymentMethod": payment_method,
                "depositPercent": deposit_percent if payment_method == "hire purchase" else None,
            },
        )

    def serve_file(self, file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        data = file_path.read_bytes()
        content_type = CONTENT_TYPES.get(file_path.suffix.lower(), "application/octet-stream")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


def run() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 3000), CarYardHandler)
    print("Car yard app running on http://localhost:3000")
    server.serve_forever()


if __name__ == "__main__":
    run()
