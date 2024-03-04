import * as React from "react";

import NiceModal from "@ebay/nice-modal-react";
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import { Helmet } from "react-helmet";
import ErrorBoundary from "../utils/ErrorBoundary";
import GlobalAppContext from "../utils/GlobalAppContext";
import { getPageProps } from "../utils/utils";
import getSettingsRoutes from "./routes";
import getRedirectRoutes from "./routes/redirectRoutes";

document.addEventListener("DOMContentLoaded", async () => {
  const { domContainer, globalAppContext, sentryProps } = await getPageProps();
  const { sentry_dsn, sentry_traces_sample_rate } = sentryProps;

  if (sentry_dsn) {
    Sentry.init({
      dsn: sentry_dsn,
      integrations: [new Integrations.BrowserTracing()],
      tracesSampleRate: sentry_traces_sample_rate,
    });
  }

  const routes = getSettingsRoutes();
  const redirectRoutes = getRedirectRoutes();
  const router = createBrowserRouter([...routes, ...redirectRoutes]);

  const renderRoot = createRoot(domContainer!);
  renderRoot.render(
    <ErrorBoundary>
      <ToastContainer
        position="bottom-right"
        autoClose={5000}
        hideProgressBar
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnHover
        theme="light"
      />
      <GlobalAppContext.Provider value={globalAppContext}>
        <NiceModal.Provider>
          <Helmet
            defaultTitle="ListenBrainz"
            titleTemplate="%s - ListenBrainz"
          />
          <RouterProvider router={router} />
        </NiceModal.Provider>
      </GlobalAppContext.Provider>
    </ErrorBoundary>
  );
});
