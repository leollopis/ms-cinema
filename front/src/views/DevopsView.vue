<template>
  <section class="card">
    <header class="board-head">
      <div>
        <p class="eyebrow">Pilotage</p>
        <h2>DevOps board</h2>
        <p class="lead">
          Ping, DB-test et contrôle start/stop via l'admin service.
        </p>
      </div>
      <div class="legend">
        <span class="pill ok">OK</span>
        <span class="pill error">Erreur</span>
        <span class="pill">—</span>
      </div>
    </header>

    <div class="grid">
      <article v-for="svc in servicesState" :key="svc.key" class="svc">
        <div class="svc-head">
          <div>
            <p class="eyebrow">{{ svc.key }}</p>
            <h3>{{ svc.name }}</h3>
          </div>
          <div class="chips">
            <span class="pill" :class="pillClass(svc.pingStatus)"
              >API {{ label(svc.pingStatus) }}</span
            >
            <span class="pill" :class="pillClass(svc.dbStatus)"
              >DB {{ label(svc.dbStatus) }}</span
            >
            <span class="pill" :class="pillClass(adminClass(svc.adminState))"
              >Admin {{ svc.adminState || "?" }}</span
            >
          </div>
        </div>

        <p class="note" v-if="svc.lastMessage">{{ svc.lastMessage }}</p>

        <div class="actions">
          <button
            class="button"
            :disabled="!svc.helloPath || svc.loading"
            @click="ping(svc)"
          >
            Ping /hello
          </button>
          <button
            class="button secondary"
            :disabled="!svc.dbPath || svc.loading"
            @click="dbTest(svc)"
          >
            DB test
          </button>
          <button
            class="button secondary"
            :disabled="!svc.admin || svc.loading"
            @click="adminAction(svc, 'start')"
          >
            Start
          </button>
          <button
            class="button secondary"
            :disabled="!svc.admin || svc.loading"
            @click="adminAction(svc, 'stop')"
          >
            Stop
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive } from "vue";

const services = [
  {
    key: "catalog",
    name: "Catalog (PHP)",
    base: "http://localhost:4001",
    helloPath: "/hello",
    dbPath: "/db-test",
    admin: true,
  },
  {
    key: "auth",
    name: "Auth (FastAPI)",
    base: "http://localhost:4002",
    helloPath: "/hello",
    dbPath: "/db-test",
    admin: true,
  },
  {
    key: "booking",
    name: "Booking (Nest)",
    base: "http://localhost:4003",
    helloPath: "/hello",
    dbPath: "/db-test",
    admin: true,
  },
];

const servicesState = reactive(
  services.map((svc) => ({
    ...svc,
    pingStatus: "unknown",
    dbStatus: "unknown",
    adminState: "?",
    lastMessage: "",
    loading: false,
  }))
);

const label = (status) => {
  if (status === "ok") return "ok";
  if (status === "error") return "err";
  return "—";
};

const pillClass = (status) => {
  if (status === "ok") return "ok";
  if (status === "error") return "error";
  return "";
};

const adminClass = (state) => {
  if (!state || state === "?") return "unknown";
  return state === "running" ? "ok" : "error";
};

const withApi = (svc, path) => {
  if (!path) return null;
  if (svc.base) return `${svc.base}${path.startsWith("/") ? path : `/${path}`}`;
  return path;
};

const safeFetch = async (svc, path, options) => {
  const url = withApi(svc, path);
  if (!url) throw new Error("missing url");
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }
  return res.text();
};

const setState = (svc, patch) => Object.assign(svc, patch);

const ping = async (svc) => {
  if (!svc.helloPath) return;
  setState(svc, { loading: true, lastMessage: "" });
  try {
    await safeFetch(svc, svc.helloPath);
    setState(svc, { pingStatus: "ok", lastMessage: "Ping OK" });
  } catch (err) {
    setState(svc, { pingStatus: "error", lastMessage: err.message });
  } finally {
    setState(svc, { loading: false });
  }
};

const dbTest = async (svc) => {
  if (!svc.dbPath) return;
  setState(svc, { loading: true, lastMessage: "" });
  try {
    await safeFetch(svc, svc.dbPath);
    setState(svc, { dbStatus: "ok", lastMessage: "DB OK" });
  } catch (err) {
    setState(svc, { dbStatus: "error", lastMessage: err.message });
  } finally {
    setState(svc, { loading: false });
  }
};

const refreshAdmin = async (svc) => {
  if (!svc.admin) return;
  try {
    const data = await safeFetch(
      { base: "http://localhost:4010" },
      `/admin/${svc.key}/status`
    );
    const state = data?.state || "?";
    setState(svc, { adminState: state });
  } catch (err) {
    setState(svc, { adminState: "error", lastMessage: err.message });
  }
};

const adminAction = async (svc, action) => {
  if (!svc.admin) return;
  setState(svc, { loading: true, lastMessage: "" });
  try {
    await safeFetch(
      { base: "http://localhost:4010" },
      `/admin/${svc.key}/${action}`,
      { method: "POST" }
    );
    await refreshAdmin(svc);
    setState(svc, { lastMessage: `${action} ok` });
  } catch (err) {
    setState(svc, { lastMessage: err.message });
  } finally {
    setState(svc, { loading: false });
  }
};

const bootstrap = async () => {
  await Promise.all(
    servicesState.map(async (svc) => {
      if (svc.helloPath) await ping(svc);
      if (svc.dbPath) await dbTest(svc);
      if (svc.admin) await refreshAdmin(svc);
    })
  );
};

onMounted(() => {
  bootstrap();
});
</script>

<style scoped>
.board-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 12px;
}

.lead {
  color: #475569;
  margin: 4px 0 0;
}

.legend {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.svc {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px;
}

.svc-head {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
}

.svc h3 {
  margin: 6px 0 0;
}

.chips {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.note {
  margin: 0;
  color: #475569;
  min-height: 18px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

@media (max-width: 720px) {
  .svc-head {
    flex-direction: column;
    align-items: flex-start;
  }
  .chips {
    justify-content: flex-start;
  }
  .board-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
