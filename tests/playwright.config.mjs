import { defineConfig } from "@playwright/test";

/* Chromium sans affichage, avec rendu WebGL logiciel (§ 12.1 a).
   Les drapeaux sont a readapter si la version de Chromium change : c'est un point de vigilance,
   pas un acquis. */
export default defineConfig({
  testDir: ".",
  testMatch: /.*\.spec\.mjs/,
  timeout: 90_000,
  reporter: [["list"]],
  fullyParallel: false,
  workers: 1,
  use: {
    headless: true,
    viewport: { width: 1280, height: 900 },
    launchOptions: {
      args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader",
             "--disable-lcd-text", "--force-device-scale-factor=1"],
    },
  },
});
