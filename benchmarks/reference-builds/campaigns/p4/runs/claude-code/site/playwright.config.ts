import { defineConfig, devices } from "@playwright/test";

const CHROMIUM = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  workers: 1,
  reporter: [["list"], ["json", { outputFile: "../evidence/browser/playwright-report.json" }]],
  timeout: 60_000,
  use: {
    baseURL: process.env.ASTERIA_BASE_URL ?? "http://localhost:3100",
    launchOptions: { executablePath: CHROMIUM },
    trace: "off",
    screenshot: "off",
  },
  projects: [
    {
      name: "desktop-chromium",
      use: { ...devices["Desktop Chrome"], launchOptions: { executablePath: CHROMIUM } },
    },
  ],
});
