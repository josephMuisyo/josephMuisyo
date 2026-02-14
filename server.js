const http = require('http');
const fs = require('fs');
const path = require('path');
const { cars } = require('./public/data/cars');

const PORT = process.env.PORT || 3000;
const publicDir = path.join(__dirname, 'public');

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
};

const sendJson = (res, statusCode, payload) => {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
};

const serveStaticFile = (res, filePath) => {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }

    const extension = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': contentTypes[extension] || 'application/octet-stream' });
    res.end(data);
  });
};

const parseBody = (req) =>
  new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += chunk;
    });
    req.on('end', () => {
      if (!raw) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/api/cars') {
    sendJson(res, 200, {
      total: cars.length,
      brands: [...new Set(cars.map((car) => car.brand))],
      cars,
    });
    return;
  }

  if (req.method === 'POST' && url.pathname === '/api/checkout') {
    try {
      const body = await parseBody(req);
      const { carId, paymentMethod, depositPercent } = body;
      const allowedPayments = ['cash', 'bank transfer', 'cheque', 'hire purchase'];

      if (!carId || !paymentMethod) {
        sendJson(res, 400, { message: 'carId and paymentMethod are required.' });
        return;
      }

      if (!allowedPayments.includes(paymentMethod)) {
        sendJson(res, 400, { message: 'Unsupported payment method.' });
        return;
      }

      const selectedCar = cars.find((car) => car.id === carId);
      if (!selectedCar) {
        sendJson(res, 404, { message: 'Selected car was not found.' });
        return;
      }

      if (paymentMethod === 'hire purchase') {
        if (typeof depositPercent !== 'number' || Number.isNaN(depositPercent)) {
          sendJson(res, 400, { message: 'Hire purchase requires a numeric depositPercent.' });
          return;
        }

        if (depositPercent < 30) {
          sendJson(res, 400, {
            message: 'Hire purchase deposit must be at least 30 percent of the car value.',
          });
          return;
        }
      }

      sendJson(res, 200, {
        message: 'Checkout accepted.',
        selectedCar,
        paymentMethod,
        depositPercent: paymentMethod === 'hire purchase' ? depositPercent : null,
      });
      return;
    } catch (error) {
      sendJson(res, 400, { message: 'Invalid JSON body.' });
      return;
    }
  }

  const routeMap = {
    '/': 'index.html',
    '/selection': 'selection.html',
    '/checkout': 'checkout.html',
  };

  if (req.method === 'GET' && routeMap[url.pathname]) {
    serveStaticFile(res, path.join(publicDir, routeMap[url.pathname]));
    return;
  }

  if (req.method === 'GET') {
    const normalized = path.normalize(url.pathname).replace(/^\/+/, '');
    const filePath = path.join(publicDir, normalized);

    if (filePath.startsWith(publicDir)) {
      serveStaticFile(res, filePath);
      return;
    }
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`Car yard app running on http://localhost:${PORT}`);
});
