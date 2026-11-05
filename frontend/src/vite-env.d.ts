/// <reference types="vite/client" />

/*
Environment variables the frontend reads from frontend/.env.
Only variables starting with VITE_ are exposed to the app.
*/
interface ImportMetaEnv {
    /*
    Backend base URL, e.g. http://localhost:8000.
    Optional: see src/api/config.ts for the default.
    */
    readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
