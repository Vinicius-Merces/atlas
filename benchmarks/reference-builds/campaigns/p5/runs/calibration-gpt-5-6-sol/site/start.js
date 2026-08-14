const { createApp } = require('./server');
const { RelayStore } = require('./src/tenant-repository');

const port = Number(process.env.PORT || 4173);
const store = new RelayStore();
const { server } = createApp({ store });

server.listen(port, '0.0.0.0', () => {
  console.log(`RelayOps calibration listening on http://0.0.0.0:${port}`);
});

function shutdown() {
  server.close(() => {
    store.close();
    process.exit(0);
  });
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
