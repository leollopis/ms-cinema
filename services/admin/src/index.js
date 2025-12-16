const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors");
const Docker = require("dockerode");

const APP_PORT = Number(process.env.APP_PORT || 4010);
const mapEnv = process.env.ALLOWED_SERVICES || "";
const allowed = Object.fromEntries(
  mapEnv
    .split(",")
    .map((p) => p.trim())
    .filter(Boolean)
    .map((p) => p.split(":"))
);

const docker = new Docker({ socketPath: "/var/run/docker.sock" });

// Allow front dev server to call admin API directly
fastify.register(cors, {
  origin: "*",
  credentials: false,
});

const getContainer = (serviceKey) => {
  const containerName = allowed[serviceKey];
  if (!containerName) return null;
  return docker.getContainer(containerName);
};

const getState = async (serviceKey) => {
  const c = getContainer(serviceKey);
  if (!c) throw new Error("service_not_allowed");
  const info = await c.inspect();
  return info?.State?.Status || "unknown";
};

const stopService = async (serviceKey) => {
  const c = getContainer(serviceKey);
  if (!c) throw new Error("service_not_allowed");
  const state = await getState(serviceKey);
  if (state === "exited" || state === "dead") return "already_stopped";
  await c.stop({ t: 2 });
  return "stopped";
};

const startService = async (serviceKey) => {
  const c = getContainer(serviceKey);
  if (!c) throw new Error("service_not_allowed");
  const state = await getState(serviceKey);
  if (state === "running") return "already_running";
  await c.start();
  return "started";
};

// Support both /admin/:service/... (intended) and /:service/... (when proxy strips prefix)
const routes = ["/admin/:service/stop", "/:service/stop"];

const startRoutes = ["/admin/:service/start", "/:service/start"];

const statusRoutes = ["/admin/:service/status", "/:service/status"];

routes.forEach((path) => {
  fastify.post(path, async (request, reply) => {
    const key = request.params.service;
    try {
      const result = await stopService(key);
      return { status: "ok", result };
    } catch (err) {
      fastify.log.error({ err }, "stop failed");
      const code = err.message === "service_not_allowed" ? 400 : 500;
      return reply.code(code).send({ status: "error", message: err.message });
    }
  });
});

startRoutes.forEach((path) => {
  fastify.post(path, async (request, reply) => {
    const key = request.params.service;
    try {
      const result = await startService(key);
      return { status: "ok", result };
    } catch (err) {
      fastify.log.error({ err }, "start failed");
      const code = err.message === "service_not_allowed" ? 400 : 500;
      return reply.code(code).send({ status: "error", message: err.message });
    }
  });
});

statusRoutes.forEach((path) => {
  fastify.get(path, async (request, reply) => {
    const key = request.params.service;
    try {
      const state = await getState(key);
      return { status: "ok", state };
    } catch (err) {
      const code = err.message === "service_not_allowed" ? 400 : 500;
      return reply.code(code).send({ status: "error", message: err.message });
    }
  });
});

const start = async () => {
  try {
    await fastify.listen({ host: "0.0.0.0", port: APP_PORT });
  } catch (err) {
    fastify.log.error({ err }, "admin service failed to start");
    process.exit(1);
  }
};

start();
